---
status: stub
---

# MCP Troubleshooting & FAQ

Common errors, diagnosing connection failures, and debugging stdio communication.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Common Issues

### 1. `uvx: command not found`
Ensure `uv` is installed and available in your global PATH:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Missing or Invalid `COT_API_KEY`
Ensure `COT_API_KEY` is set in the `env` dictionary of your client's config file, and that your account possesses an active **Quant Tier** subscription.

### 3. Server Exits Immediately
You can test the MCP server directly in your terminal using the MCP inspector:
```bash
npx @modelcontextprotocol/inspector uvx "cotbias[mcp]" cotbias-mcp
```

## Roadmap & Upcoming Content
- [ ] Inspecting Claude Desktop and Cursor log files.
- [ ] Error envelope parsing by the LLM.
- [ ] Submitting bug reports and diagnostic information.
