---
status: stub
---

# Claude Desktop Integration

Step-by-step setup guide for integrating `cotbias-mcp` with Anthropic's Claude Desktop application on macOS and Windows.

!!! note "Documentation in Progress"
    This guide is currently being drafted as part of our Phase 2 documentation rollout.

## Quick Setup

Add the following to your `claude_desktop_config.json`:

```json
--8<-- "docs/snippets/mcp-config.json"
```

### Config File Locations
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## Roadmap & Upcoming Content
- [ ] Verifying server startup in Claude logs.
- [ ] Sample chat prompts for macro briefings and market snapshots.
- [ ] Managing `COT_API_KEY` security.
- [ ] Troubleshooting common connection issues.
