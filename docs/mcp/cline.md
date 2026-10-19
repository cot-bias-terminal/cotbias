---
status: stub
---

# Cline & Other MCP Clients

Integration instructions for Cline (VS Code extension), LibreChat, Windsurf, and custom Model Context Protocol clients.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Quick Setup

Add the following standard entry into your client's MCP server configuration:

```json
--8<-- "docs/snippets/mcp-config.json"
```

!!! warning "Hosted Clients Note"
    Remote web clients such as ChatGPT or Gemini Web do not currently support local stdio MCP servers directly. They require a hosted remote MCP server with authentication, which is planned for a future release.

## Roadmap & Upcoming Content
- [ ] Cline configuration and permission workflows.
- [ ] LibreChat docker integration patterns.
- [ ] Stdio client debugging and protocol verification.
