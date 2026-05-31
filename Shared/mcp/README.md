# PortableLM MCP Fast 3.2 — Connection Guide

This directory contains the MCP (Model Context Protocol) Fast 3.2 configuration for PortableLM.

## What is MCP?

MCP is the protocol used by modern AI models (Claude 4.5+, Codex 5.5+, Qwen3+) to call tools,
read files, run commands, and interact with external systems in a structured, permission-scoped way.

PortableLM runs a **local MCP server** on port `3334` alongside the chat server on `3333`.
All tools in `registry.json` are available to any connected MCP client.

## Connecting Your IDE / Client

### KiloCode
In KiloCode settings → MCP Servers → Add:
```json
{
  "mcpServers": {
    "portablelm": {
      "url": "http://localhost:3334/mcp",
      "transport": "http"
    }
  }
}
```

### VS Code (with MCP extension)
Add to `.vscode/settings.json` or user `settings.json`:
```json
{
  "mcp.servers": {
    "portablelm": {
      "url": "http://localhost:3334/mcp",
      "transport": "http"
    }
  }
}
```

### Cursor
Add to Cursor settings → MCP → Add Server:
```json
{
  "mcpServers": {
    "portablelm": {
      "url": "http://localhost:3334/mcp",
      "transport": "http"
    }
  }
}
```

### Claude Desktop
Add to `%APPDATA%\Claude\claude_desktop_config.json` (Windows):
```json
{
  "mcpServers": {
    "portablelm": {
      "command": "python3",
      "args": ["C:/path/to/USB/Shared/mcp/server.py"]
    }
  }
}
```

## Tool Permission Model

| Approval Level | Behaviour |
|---|---|
| `requires_approval: false` | Executes immediately, result returned inline |
| `requires_approval: true` | Pauses and prompts for confirmation in chat UI |
| `authorization_required: true` | Also requires explicit target scope declaration |

Tools are additionally scoped to **security profiles** via `allowed_profiles`.
A `redteam`-only tool will not execute under the `default` or `ir` profile.

## Security Profile → Tool Access Matrix

| Tool | default | cybersec | redteam | bugbounty | ir | devsecops |
|---|---|---|---|---|---|---|
| shell_exec | ✗ | ✓ | ✓ | ✓ | ✓ | ✗ |
| file_reader | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| file_writer | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| nuclei_scan | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| sigma_rule_gen | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ |
| yara_scan | ✗ | ✓ | ✓ | ✗ | ✓ | ✗ |
| mitre_lookup | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| web_fetch | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| cve_lookup | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| hash_check | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| port_scan | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ |
| report_gen | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

## Remote Integrations

Set the relevant environment variable before launching `start.sh` / `start-fast-chat.bat`:

| Integration | Env Var | Purpose |
|---|---|---|
| GitHub | `GITHUB_TOKEN` | Repo access, issue/PR creation |
| Jira | `JIRA_API_TOKEN` | Ticket creation from findings |
| Slack | `SLACK_BOT_TOKEN` | Alert notifications |

## Skills

Custom reusable workflows live in `Shared/skills/`.
See `Shared/skills/README.md` for the full skill schema and creation guide.
