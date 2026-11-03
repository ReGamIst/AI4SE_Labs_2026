#!/usr/bin/env python3
"""Implement missing methods with the RAG pipeline, then run the unit tests.

For each task in missing_code.json, this script finds the 5 best-matching chunks,
sends the task and chunks to an OpenAI model, and writes the returned code into
the target file. If unit tests fail, it retries the responsible methods with the
failure details.

Setup (Python 3.10-3.13):

    python -m pip install openai==3.42.1 wordllama==0.4.0.post1
    python chunk_playground.py
    python embed_chunks.py

Usage, from anywhere:

    python solve_tasks.py                      # asks for your key once if needed
    python solve_tasks.py --model gpt-5.6-luna
    python solve_tasks.py --dry-run            # no key, no API call, no file changes

The key is read from the OPENAI_API_KEY environment variable. If that isn't set,
the script asks for it with hidden input and keeps it in memory for this run only.
"""

from __future__ import annotations

import argparse
import ast
import getpass
import inspect
import json
import logging
import os
import re
import subprocess
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from embed_chunks import DEFAULT_CHUNKS, DEFAULT_INDEX, load_store

ALLOWED_MODELS = (
    "gpt-6-luna",
    "gpt-5.6-luna",
    "gpt-5.4-nano",
    "gpt-5-nano",
    "gpt-5-mini",
    "gpt-4.1-nano",
    "gpt-4o-mini",
)
DEFAULT_MODEL = "gpt-6-luna"
TOP_K = 5
MAX_OUTPUT_TOKENS = 4000
DEFAULT_REPAIR_ROUNDS = 2
DEFAULT_TEST_TIMEOUT = 120  # Generated code could loop forever.
MAX_FEEDBACK_CHARS = 3000

RAG_DIR = Path(__file__).resolve().parent
REPO_DIR = RAG_DIR.parent
TESTS_ROOT = REPO_DIR / "playground"
SOURCE_ROOT = TESTS_ROOT / "playground"
DEFAULT_TASKS = RAG_DIR / "missing_code.json"

SYSTEM_PROMPT = """\
You implement one missing method in an existing Python code base.

Return only the complete method, starting with its `def` line, in one Python code \
block. Rules:
- Keep the given signature exactly.
- Use only names that are imported in the file, or that the context shows exist. \
Do not add module-level imports.
- Follow the conventions in the context, such as how invalid input is handled.
- Unit tests define the required behaviour. If a test and the task description \
disagree, follow the test.
- Do not include tests, explanations or other methods."""


class TaskError(Exception):
    """A problem with one task. The model can be asked again."""


class ApiError(Exception):
    """A problem talking to the API, which would affect every task."""


@dataclass(frozen=True)
class Task:
    """One entry in the tasks file."""

    file: str
    class_name: str
    method: str
    docstring: str  # The cleaned docstring text, without quotes.

    @property
    def label(self) -> str:
        return f"{self.class_name}.{self.method}"

    @property
    def path(self) -> Path:
        return REPO_DIR / self.file


@dataclass
class Feedback:
    """What went wrong last time, for a retry."""

    message: str
    test_names: List[str] = field(default_factory=list)


@dataclass
class TestRun:
    passed: bool
    summary: str
    output: str


# Tasks -----------------------------------------------------------------------


def load_tasks(path: Path) -> List[Task]:
    """Read and validate the tasks file."""
    if not path.is_file():
        raise SystemExit(f"Tasks file not found: {path}")
    tasks = []
    for number, entry in enumerate(json.loads(path.read_text(encoding="utf-8-sig")), 1):
        try:
            # The file's indentation varies, so only the docstring's value is kept.
            value = ast.literal_eval(entry["docstring"].strip())
            task = Task(entry["file"], entry["class"], entry["method"], inspect.cleandoc(value))
        except (KeyError, TypeError, ValueError, SyntaxError) as error:
            raise SystemExit(f"Task {number} in {path} is invalid: {error}") from None
        if not task.path.resolve().is_relative_to(SOURCE_ROOT):
            raise SystemExit(f"Task {number} targets a file outside {SOURCE_ROOT}: {task.file}")
        tasks.append(task)
    return tasks


def task_text(task: Task) -> str:
    """Write a task as text. It's used both as the search query and in the prompt.

    Naming the likely tests matters: without these words, top-5 retrieval found
    the relevant test chunk for only 4 of the 10 tasks, compared with all 10 here.
    """
    return (
        f"Implement {task.label}. {task.docstring} "
        f"{task.class_name}Tests test_{task.method.strip('_')}"
    )


# Reading and writing source files --------------------------------------------


def read_source(path: Path) -> str:
    """Read a file with LF line endings, or raise TaskError."""
    try:
        return path.read_bytes().decode("utf-8-sig").replace("\r\n", "\n")
    except (OSError, UnicodeDecodeError) as error:
        raise TaskError(f"Cannot read {path}: {error}") from None


def write_source(path: Path, source: str) -> None:
    """Replace a file in one step, keeping its line endings and byte order mark."""
    original = path.read_bytes()
    if b"\r\n" in original:
        source = source.replace("\n", "\r\n")
    data = source.encode("utf-8")
    if original.startswith(b"\xef\xbb\xbf"):
        data = b"\xef\xbb\xbf" + data
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(data)
    os.replace(temporary, path)


def find_method(tree: ast.AST, task: Task) -> ast.FunctionDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == task.class_name:
            for member in node.body:
                if (
                    isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and member.name == task.method
                ):
                    return member
    raise TaskError(f"{task.label} was not found in {task.file}")


def statements_without_docstring(node: ast.AST) -> List[ast.stmt]:
    body = list(node.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    return body


def is_stub(statements: Sequence[ast.stmt]) -> bool:
    """Tell whether a function body has no real implementation."""
    if not statements:
        return True
    if len(statements) > 1:
        return False
    statement = statements[0]
    if isinstance(statement, ast.Pass):
        return True
    if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant):
        return True
    return isinstance(statement, ast.Raise) and "NotImplementedError" in ast.dump(statement)


def parse_source(source: str, task: Task) -> ast.Module:
    try:
        return ast.parse(source)
    except SyntaxError as error:
        raise TaskError(f"{task.file} has a syntax error: {error}") from None


def needs_implementation(task: Task) -> bool:
    node = find_method(parse_source(read_source(task.path), task), task)
    return is_stub(statements_without_docstring(node))


def method_source(source: str, node: ast.FunctionDef) -> str:
    lines = source.split("\n")
    first = min([node.lineno] + [d.lineno for d in node.decorator_list])
    return textwrap.dedent("\n".join(lines[first - 1:node.end_lineno]))


def describe_target(task: Task, source: str) -> str:
    """Give the model the exact signature and the names available in the file."""
    tree = ast.parse(source)
    node = find_method(tree, task)
    lines = source.split("\n")
    first = min([node.lineno] + [d.lineno for d in node.decorator_list])
    last = max(node.body[0].lineno - 1, node.lineno)
    signature = textwrap.dedent("\n".join(lines[first - 1:last]))
    imports = [
        "\n".join(lines[n.lineno - 1:n.end_lineno])
        for n in tree.body
        if isinstance(n, (ast.Import, ast.ImportFrom))
    ]
    return (
        f"File: {task.file}\nClass: {task.class_name}\n\n"
        f"Signature:\n{signature}\n\nImports in this file:\n" + "\n".join(imports)
    )


def extract_body(response: str, task: Task) -> List[str]:
    """Return the statements of the named method from the model's reply, unindented."""
    blocks = re.findall(r"```[ \t]*(?:python|py)?[ \t]*\r?\n(.*?)```", response, re.DOTALL)
    candidates = blocks + [response]
    for candidate in candidates:
        code = textwrap.dedent(candidate.replace("\r\n", "\n")).strip("\n")
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == task.method:
                statements = statements_without_docstring(node)
                if is_stub(statements):
                    raise TaskError("The reply's method has no implementation.")
                lines = code.split("\n")
                first = statements[0]
                decorators = getattr(first, "decorator_list", [])
                start = min([first.lineno] + [d.lineno for d in decorators])
                selected = lines[start - 1:statements[-1].end_lineno]
                if start == node.lineno:  # def f(self): return 1
                    selected[0] = selected[0][first.col_offset:]
                return textwrap.dedent("\n".join(selected)).split("\n")
    raise TaskError(f"The reply has no valid Python definition of {task.method}.")


def replace_body(source: str, task: Task, body: Sequence[str]) -> str:
    """Return the source with only the method's docstring and body replaced."""
    tree = ast.parse(source)
    node = find_method(tree, task)
    indent = " " * (node.col_offset + 4)
    docstring_lines = task.docstring.split("\n")
    docstring_lines[0] = '"""' + docstring_lines[0]
    docstring_lines[-1] += '"""'
    new_lines = [
        indent + line if line.strip() else ""
        for line in list(docstring_lines) + list(body)
    ]

    lines = source.split("\n")
    start = node.body[0].lineno
    end = node.body[-1].end_lineno
    # A stub written as "def f(self): pass" keeps its header on its own line.
    prefix = lines[start - 1][:node.body[0].col_offset]
    header = [prefix.rstrip()] if prefix.strip() else []
    updated = "\n".join(lines[:start - 1] + header + new_lines + lines[end:])

    try:
        new_tree = ast.parse(updated)
    except SyntaxError as error:
        raise TaskError(f"The code would break {task.file}: {error}") from None
    new_node = find_method(new_tree, task)
    if ast.get_docstring(new_node) != task.docstring:
        raise TaskError("The required docstring could not be kept.")
    # Everything except this method's body must be unchanged.
    node.body, new_node.body = [], []
    if ast.dump(tree) != ast.dump(new_tree):
        raise TaskError(f"The code would change other parts of {task.file}.")
    return updated


# Prompt and model ------------------------------------------------------------


def build_prompt(
    task: str, target: str, chunks: Sequence[dict], current: str, feedback: Optional[Feedback]
) -> str:
    """Combine the task, target details and retrieved chunks into one prompt."""
    context = "\n\n".join(
        f"--- Chunk {number}: {chunk['id']} ({chunk['role']})\n{chunk['context']}\n{chunk['text']}"
        for number, chunk in enumerate(chunks, 1)
    )
    prompt = f"# Task\n{task}\n\n# Target\n{target}\n\n# Context from the code base\n{context}\n"
    if feedback:
        prompt += (
            f"\n# Previous attempt\nThe previous code was:\n{current}\n\n"
            f"It failed with:\n{feedback.message[:MAX_FEEDBACK_CHARS]}\n"
            "Fix the method so that this no longer happens.\n"
        )
    return prompt


def create_client(api_key: str):
    try:
        from openai import OpenAI
    except ImportError:
        raise SystemExit(
            "The openai package is missing. Install it with:\n"
            "    python -m pip install openai==3.42.1"
        ) from None
    return OpenAI(api_key=api_key, timeout=120, max_retries=3)


def get_api_key() -> str:
    """Use the environment variable, or ask once with hidden input."""
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        key = getpass.getpass("Enter your OpenAI API key (input is hidden): ").strip()
    if not key:
        raise SystemExit("No API key was given.")
    return key


def call_model(client, model: str, prompt: str) -> tuple:
    """Send one prompt. Return the reply and the number of tokens used."""
    from openai import OpenAIError

    try:
        response = client.responses.create(
            model=model,
            instructions=SYSTEM_PROMPT,
            input=prompt,
            max_output_tokens=MAX_OUTPUT_TOKENS,
            store=False,
        )
    except OpenAIError as error:
        message = str(error)
        if client.api_key:
            message = message.replace(client.api_key, "***")
        raise ApiError(f"{type(error).__name__}: {message}") from None
    if response.status != "completed":
        raise TaskError(f"The reply was not completed (status: {response.status}).")
    usage = response.usage
    tokens = (usage.input_tokens + usage.output_tokens) if usage else 0
    return response.output_text, tokens


# The pipeline ----------------------------------------------------------------


def solve_task(
    task_description: str,
    target: Task,
    store,
    client,
    model: str,
    feedback: Optional[Feedback] = None,
) -> int:
    """Solve one task: match chunks, ask the model, write the code to the file.

    Returns the number of tokens used. Raises TaskError, leaving the file unchanged,
    if the reply can't be used.
    """
    query = task_description
    if feedback and feedback.test_names:
        query += " Failing tests: " + " ".join(feedback.test_names[:5])
    chunks = [result.chunk for result in store.search(query, k=TOP_K)]

    source = read_source(target.path)
    node = find_method(parse_source(source, target), target)
    prompt = build_prompt(
        task_description,
        describe_target(target, source),
        chunks,
        method_source(source, node),
        feedback,
    )
    reply, tokens = call_model(client, model, prompt)
    write_source(target.path, replace_body(source, target, extract_body(reply, target)))
    return tokens


def run_unit_tests(timeout: int) -> TestRun:
    """Run the whole test suite in a separate process."""
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    environment.pop("OPENAI_API_KEY", None)  # The tests don't need the key.
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
            cwd=TESTS_ROOT,
            env=environment,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return TestRun(False, f"Tests did not finish within {timeout} s", "")
    output = result.stderr + result.stdout
    ran = re.search(r"Ran (\d+) tests?", output)
    count = int(ran.group(1)) if ran else 0
    lines = [line for line in output.strip().split("\n") if line.strip()]
    summary = f"{count} tests run, {lines[-1] if lines else 'no output'}"
    return TestRun(result.returncode == 0 and count > 0, summary, output)


def failure_blocks(output: str) -> List[str]:
    return [
        block.strip()
        for block in re.split(r"^={20,}$", output, flags=re.MULTILINE)
        if re.match(r"\s*(FAIL|ERROR):", block)
    ]


def is_implicated(task: Task, block: str) -> bool:
    """Tell whether a test failure looks related to a task's method."""
    file_name = Path(task.file).name
    if re.search(rf'{re.escape(file_name)}", line \d+, in {re.escape(task.method)}\b', block):
        return True
    if not task.method.startswith("__") and re.search(rf"\.{re.escape(task.method)}\b", block):
        return True
    heading = block.split("\n", 1)[0]
    match = re.search(r"(?:FAIL|ERROR): (\w+) \([\w.]*?(\w+Tests)\b", heading)
    return bool(
        match
        and match.group(2).startswith(task.class_name)
        and task.method.strip("_") in match.group(1)
    )


def plan_repairs(tasks: Sequence[Task], run: TestRun) -> Dict[Task, Feedback]:
    """Choose which tasks to retry after failed tests, and with what information."""
    blocks = failure_blocks(run.output)
    repairs: Dict[Task, Feedback] = {}
    for task in tasks:
        related = [block for block in blocks if is_implicated(task, block)]
        if related:
            names = [
                match.group(1)
                for match in (re.search(r"(?:FAIL|ERROR): (\w+)", b) for b in related)
                if match
            ]
            repairs[task] = Feedback("\n\n".join(related), names)
    if not repairs:  # Examples: a timeout, or a failure that names no method.
        message = run.output[-MAX_FEEDBACK_CHARS:] or run.summary
        repairs = {task: Feedback(message) for task in tasks}
    return repairs


def solve_all(
    tasks: Sequence[Task], model: str, rounds: int, test_timeout: int, store=None
) -> bool:
    """Solve all tasks and repair them until the unit tests pass or rounds run out."""
    store = store or load_store(DEFAULT_INDEX, DEFAULT_CHUNKS)
    client = None
    total_tokens = 0
    pending: Dict[Task, Optional[Feedback]] = {}
    errors: Dict[Task, str] = {}
    for task in tasks:
        try:
            if needs_implementation(task):
                pending[task] = None
            else:
                print(f"Already implemented: {task.label}")
        except TaskError as error:
            errors[task] = str(error)
            print(f"Failed: {task.label}: {error}")

    for round_number in range(rounds + 1):
        if pending and client is None:
            client = create_client(get_api_key())
        for task, feedback in pending.items():
            errors.pop(task, None)
            try:
                total_tokens += solve_task(task_text(task), task, store, client, model, feedback)
                print(f"Wrote: {task.label} ({task.file})")
            except TaskError as error:
                errors[task] = str(error)
                print(f"Failed: {task.label}: {error}")

        run = run_unit_tests(test_timeout)
        print(f"Unit tests: {run.summary}")
        if run.passed and not errors:
            print(f"Done. All tests pass. Model: {model}. Tokens used: {total_tokens}.")
            return True

        pending = {} if run.passed else plan_repairs(tasks, run)
        for task, message in errors.items():
            if task.path.is_file():
                pending.setdefault(task, Feedback(message))
        if round_number < rounds and pending:
            names = ", ".join(task.label for task in pending)
            print(f"Retrying ({round_number + 1} of {rounds}): {names}")

    print(f"\nNot finished. Tokens used: {total_tokens}.")
    for task, message in errors.items():
        print(f"- {task.label}: {message}")
    if not run.passed:
        print("\nLast test output:\n" + run.output[-MAX_FEEDBACK_CHARS:])
    return False


def dry_run(tasks: Sequence[Task]) -> None:
    """Show what would be sent, without a key, an API call or file changes."""
    store = load_store(DEFAULT_INDEX, DEFAULT_CHUNKS)
    for task in tasks:
        print(f"\n{task.label}\n  Task: {task_text(task)}")
        for result in store.search(task_text(task), k=TOP_K):
            print(f"  - {result.chunk['id']}")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"default: {DEFAULT_MODEL}")
    parser.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    parser.add_argument(
        "--repair-rounds", type=int, default=DEFAULT_REPAIR_ROUNDS,
        help="how many times to retry after failed tests (default %(default)s)",
    )
    parser.add_argument(
        "--test-timeout", type=int, default=DEFAULT_TEST_TIMEOUT,
        help="seconds allowed for one test run (default %(default)s)",
    )
    parser.add_argument("--dry-run", action="store_true", help="show matched chunks only")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    logging.disable(logging.INFO)  # Keeps per-request HTTP logs out of the output.
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.model not in ALLOWED_MODELS:
        print(
            f"Model not allowed: {args.model}\nAllowed: {', '.join(ALLOWED_MODELS)}",
            file=sys.stderr,
        )
        return 2
    if args.repair_rounds < 0 or args.test_timeout <= 0:
        print("--repair-rounds and --test-timeout are out of range", file=sys.stderr)
        return 2
    tasks = load_tasks(args.tasks)
    if args.dry_run:
        dry_run(tasks)
        return 0
    try:
        return 0 if solve_all(tasks, args.model, args.repair_rounds, args.test_timeout) else 1
    except ApiError as error:
        print(f"\nStopped because of an API error: {error}", file=sys.stderr)
        print("Methods written so far stay in place. Rerunning continues from there.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
