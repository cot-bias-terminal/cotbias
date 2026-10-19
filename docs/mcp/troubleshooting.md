# MCP Troubleshooting & Diagnostics

This guide resolves common connection issues, environment configuration problems, and execution errors when running `cotbias-mcp`.

---

## 🔧 Common Issues & Solutions

### 1. `uvx: command not found`
**Cause**: The `uv` binary is installed in `~/.local/bin` or `/opt/homebrew/bin`, but the desktop application (Claude Desktop or Cursor) is launched outside a shell environment with a minimal `PATH`.

**Solution**:
1. Check where `uvx` is installed:
   ```bash
   which uvx
   ```
2. In your `claude_desktop_config.json` or `.cursor/mcp.json`, replace `"uvx"` with the absolute path:
   ```json
   {
     "mcpServers": {
       "cotbias": {
         "command": "/opt/homebrew/bin/uvx",
         "args": ["cotbias[mcp]", "cotbias-mcp"],
         "env": {
           "COT_API_KEY": "cot_live_..."
         }
       }
     }
   }
   ```

---

### 2. Authentication & Permission Errors (401 / 403)
**Error Envelope returned to agent**:
```json
{
  "error": {
    "code": "AuthenticationError",
    "message": "Invalid API key",
    "hint": "API key missing, invalid, or expired..."
  }
}
```

**Solution**:
1. Verify `COT_API_KEY` is present in the `env` dictionary of your client configuration file.
2. Confirm your key has an active **Quant Tier** subscription. Free accounts do not have access to programmatic API and MCP endpoints.

---

### 3. Testing with MCP Inspector

To test the MCP server in isolation without launching Claude or Cursor:

```bash
export COT_API_KEY="cot_live_your_actual_key"
npx @modelcontextprotocol/inspector uvx "cotbias[mcp]" cotbias-mcp
```

This launches a local web UI where you can test tool execution, review parameter schemas, and inspect raw JSON payloads.

---

## 🪵 Client Log File Locations

If the MCP server fails to launch, inspect the client's internal logs:

### Claude Desktop Logs
- **macOS**: `~/Library/Logs/Claude/mcp*.log`
- **Windows**: `%APPDATA%\Claude\logs\mcp*.log`

To monitor logs in real-time on macOS:
```bash
tail -f ~/Library/Logs/Claude/mcp*.log
```

### Cursor Logs
1. Open Cursor's **Output** panel (`Cmd + Shift + U` / `Ctrl + Shift + U`).
2. In the dropdown at the top-right, select **MCP: cotbias**.
