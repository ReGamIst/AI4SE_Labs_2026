"""LLM access layer.

* OpenAIBackend - real calls through the OpenAI Chat Completions API (JSON mode).
* MockBackend   - deterministic heuristic stand-in used for offline debugging of
                  the graph (python run.py ... --mock). It produces schema-valid
                  outputs so every node, edge and the feedback loop can be
                  exercised without network access or cost.

Every call goes through `call_json`, which
  1. asks the model for a JSON object,
  2. validates it against a pydantic schema,
  3. on failure, feeds the validation error back to the model and retries
     (self-correction loop), and
  4. caches successful answers on disk keyed by (model, messages), so re-runs
     after a crash resume cheaply.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import threading
import time
from pathlib import Path
from typing import Type, TypeVar

from pydantic import BaseModel, ValidationError

log = logging.getLogger("reqnet.llm")
T = TypeVar("T", bound=BaseModel)

PAYLOAD_MARKER = "INPUT_JSON:"


def make_user_message(instructions: str, payload: dict) -> str:
    """User messages always carry their data as a JSON block after a marker."""
    return f"{instructions.strip()}\n\n{PAYLOAD_MARKER}\n{json.dumps(payload, ensure_ascii=False, indent=1)}"


def extract_payload(user_msg: str) -> dict:
    return json.loads(user_msg.split(PAYLOAD_MARKER, 1)[1])


def _parse_json(text: str) -> dict:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    if m:
        text = m.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object found in model output")
    return json.loads(text[start:end + 1])


class Usage:
    def __init__(self):
        self.lock = threading.Lock()
        self.by_model: dict[str, dict[str, int]] = {}

    def add(self, model: str, prompt: int, completion: int, cached: bool = False):
        with self.lock:
            d = self.by_model.setdefault(model, {"calls": 0, "cache_hits": 0,
                                                 "prompt_tokens": 0, "completion_tokens": 0})
            d["calls"] += 1
            d["cache_hits"] += int(cached)
            d["prompt_tokens"] += prompt
            d["completion_tokens"] += completion


class BaseBackend:
    def __init__(self, cache_dir: Path | None = None):
        self.cache_dir = cache_dir
        self.usage = Usage()
        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)

    # -- subclass hook ---------------------------------------------------
    def _complete(self, model: str, messages: list[dict], schema: Type[BaseModel]) -> tuple[str, int, int]:
        raise NotImplementedError

    # -- public API ------------------------------------------------------
    def call_json(self, model: str, system: str, user: str, schema: Type[T],
                  max_attempts: int = 3, tag: str = "") -> T:
        schema_hint = json.dumps(schema.model_json_schema(), ensure_ascii=False)
        messages = [
            {"role": "system", "content": system.strip() +
             "\n\nRespond with a single JSON object only (no prose, no markdown fences) "
             "that conforms to this JSON schema:\n" + schema_hint},
            {"role": "user", "content": user},
        ]
        key = hashlib.sha256(json.dumps([self.__class__.__name__, model, messages]).encode()).hexdigest()[:32]
        cfile = self.cache_dir / f"{key}.json" if self.cache_dir else None
        if cfile and cfile.exists():
            self.usage.add(model, 0, 0, cached=True)
            return schema.model_validate_json(cfile.read_text(encoding="utf-8"))

        last_err = None
        for attempt in range(1, max_attempts + 1):
            text, p, c = self._complete(model, messages, schema)
            self.usage.add(model, p, c)
            try:
                obj = schema.model_validate(_parse_json(text))
                if cfile:
                    cfile.write_text(obj.model_dump_json(indent=1), encoding="utf-8")
                return obj
            except (ValueError, ValidationError) as e:
                last_err = e
                log.warning("[%s] %s: invalid JSON on attempt %d: %s", tag, model, attempt, str(e)[:300])
                messages = messages + [
                    {"role": "assistant", "content": text[:20000]},
                    {"role": "user", "content": "Your answer did not validate against the schema:\n"
                     f"{str(e)[:2000]}\nReturn the corrected, complete JSON object only."},
                ]
        raise RuntimeError(f"[{tag}] {model}: no valid output after {max_attempts} attempts: {last_err}")


class OpenAIBackend(BaseBackend):
    def __init__(self, cache_dir: Path | None = None, reasoning_effort: str | None = None,
                 timeout: float = 600.0):
        super().__init__(cache_dir)
        from openai import OpenAI  # imported lazily so --mock works without the package configured
        if not os.environ.get("OPENAI_API_KEY"):
            raise SystemExit("OPENAI_API_KEY is not set (use --mock for an offline dry run).")
        self.client = OpenAI(timeout=timeout, max_retries=4)
        self.reasoning_effort = reasoning_effort
        self._json_mode_ok: dict[str, bool] = {}

    def _complete(self, model, messages, schema):
        kwargs = {"model": model, "messages": messages}
        if self.reasoning_effort:
            kwargs["reasoning_effort"] = self.reasoning_effort
        if self._json_mode_ok.get(model, True):
            kwargs["response_format"] = {"type": "json_object"}
        for net_attempt in range(5):
            try:
                resp = self.client.chat.completions.create(**kwargs)
                break
            except Exception as e:  # noqa: BLE001
                msg = str(e)
                if "response_format" in msg and "response_format" in kwargs:
                    log.warning("%s rejects JSON mode; retrying without it", model)
                    self._json_mode_ok[model] = False
                    kwargs.pop("response_format")
                    continue
                if "reasoning_effort" in msg and "reasoning_effort" in kwargs:
                    log.warning("%s rejects reasoning_effort; retrying without it", model)
                    kwargs.pop("reasoning_effort")
                    continue
                if net_attempt == 4:
                    raise
                wait = 5 * (net_attempt + 1)
                log.warning("%s call failed (%s); retry in %ss", model, msg[:200], wait)
                time.sleep(wait)
        u = resp.usage
        return (resp.choices[0].message.content or "",
                getattr(u, "prompt_tokens", 0) or 0, getattr(u, "completion_tokens", 0) or 0)


def build_backend(mock: bool, cache_dir: Path | None, reasoning_effort: str | None) -> BaseBackend:
    if mock:
        from .mock import MockBackend
        return MockBackend(cache_dir=None)
    return OpenAIBackend(cache_dir=cache_dir, reasoning_effort=reasoning_effort)
