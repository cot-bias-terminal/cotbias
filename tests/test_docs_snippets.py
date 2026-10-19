import json
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def test_readme_mcp_config_matches_snippet():
    snippet_path = ROOT_DIR / "docs" / "snippets" / "mcp-config.json"
    readme_path = ROOT_DIR / "README.md"

    assert snippet_path.exists(), f"Snippet not found at {snippet_path}"
    assert readme_path.exists(), f"README not found at {readme_path}"

    snippet_data = json.loads(snippet_path.read_text(encoding="utf-8"))

    readme_text = readme_path.read_text(encoding="utf-8")
    # Match ```json ... ``` blocks in README
    json_blocks = re.findall(r"```json\s*(\{.*?\})\s*```", readme_text, flags=re.DOTALL)
    assert json_blocks, "No json code blocks found in README.md"

    # Find the block containing mcpServers
    matching_block = None
    for block in json_blocks:
        try:
            data = json.loads(block)
            if "mcpServers" in data:
                matching_block = data
                break
        except json.JSONDecodeError:
            continue

    assert matching_block is not None, "mcpServers json block not found in README.md"
    assert matching_block == snippet_data, (
        f"README MCP config does not match docs/snippets/mcp-config.json:\n"
        f"README: {matching_block}\nSnippet: {snippet_data}"
    )
