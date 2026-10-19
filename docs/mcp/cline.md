# Cline & Other MCP Clients

In addition to Claude Desktop and Cursor, `cotbias-mcp` is compatible with any client implementing Anthropic's [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) over standard input/output (`stdio`).

---

## 🛠 Cline (VS Code Extension) Setup

1. Install the [Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) in VS Code.
2. In the Cline settings tab, click the **MCP Servers** icon (or open `cline_mcp_settings.json`).
3. Add the `cotbias` server configuration:

```json
--8<-- "docs/snippets/mcp-config.json"
```

4. Save the file. Cline will automatically start the server and register the tools.

---

## 🌊 Windsurf IDE Setup

In Windsurf, open your user configuration (`~/.codeium/windsurf/mcp_config.json`) and add the same configuration block under `mcpServers`.

---

## 💬 LibreChat Setup

In your `librechat.yaml` configuration file:

```yaml
mcpServers:
  cotbias:
    type: stdio
    command: uvx
    args:
      - "cotbias[mcp]"
      - "cotbias-mcp"
    env:
      COT_API_KEY: "cot_live_YOUR_ACTUAL_API_KEY"
```

---

## ⚠️ Note on Hosted Web Clients (ChatGPT, Gemini)

!!! warning "Local Stdio vs Hosted Remote Server"
    Web-based LLM interfaces such as **ChatGPT** (OpenAI) and **Gemini Web** do not currently support local `stdio` subprocess execution on your desktop machine. 

    They require a public, hosted HTTPS remote server with OAuth2 authentication. A hosted remote MCP endpoint for web-based AI clients is on the product roadmap for a future release. For now, use `cotbias-mcp` with desktop agents (**Claude Desktop**, **Cursor**, **Cline**, **Windsurf**).
