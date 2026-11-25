from mcp.server.mcpserver import MCPServer

mcp = MCPServer("text-tools")

@mcp.tool()
def count_words(text: str) -> int:
    """Count the number of words in the given text."""
    return len(text.split())

if __name__ == "__main__":
    mcp.run()