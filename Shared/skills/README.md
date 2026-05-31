# PortableLM Skills

Skills are portable, reusable workflow definitions that chain MCP tools and model calls
into named operations. They travel with the USB drive and appear automatically in the
chat UI Skills panel on launch.

## Skill Schema

```json
{
  "id": "skill_id",
  "name": "Human Readable Name",
  "description": "What this skill does",
  "version": "1.0",
  "author": "your_name",
  "required_profile": "cybersec",
  "requires_approval": true,
  "authorization_required": false,
  "model_hints": {
    "reasoning": "preferred-model-local",
    "code": "preferred-model-local"
  },
  "steps": [
    {
      "step": 1,
      "type": "model_call",
      "prompt": "Analyse the following and extract IOCs: {{input}}",
      "model_hint": "reasoning",
      "output_var": "iocs"
    },
    {
      "step": 2,
      "type": "mcp_tool",
      "tool_id": "yara_scan",
      "args": {"target": "{{input_file}}"},
      "output_var": "yara_results"
    },
    {
      "step": 3,
      "type": "model_call",
      "prompt": "Given IOCs: {{iocs}} and YARA results: {{yara_results}}, generate a Sigma rule.",
      "model_hint": "code",
      "output_var": "sigma_rule"
    },
    {
      "step": 4,
      "type": "mcp_tool",
      "tool_id": "file_writer",
      "args": {"filename": "sigma_{{timestamp}}.yml", "content": "{{sigma_rule}}"}
    }
  ]
}
```

## Step Types

| Type | Description |
|---|---|
| `model_call` | Send a prompt to the active AI model. Supports `{{variable}}` interpolation. |
| `mcp_tool` | Execute a registered MCP tool from `registry.json`. |
| `user_input` | Pause and prompt the user for additional input mid-workflow. |
| `conditional` | Branch based on a condition evaluated against a previous output variable. |

## Model Hints

`model_hint` values route to the best available model for the task:

| Hint | Best Local Model | Best Cloud Model |
|---|---|---|
| `reasoning` | `deepseek-r1-70b-local` | `venice: deepseek-r1-671b` |
| `code` | `llama33-70b-local` | `venice: claude-opus-4-5` or `codex-mini` |
| `fast` | `llama31-8b-local` | `venice: llama-3.3-70b` |
| `long_context` | `qwen3-32b-local` | `minimax: abab7-chat` |

## Built-in Starter Skills

| File | Name | Profile Required | Description |
|---|---|---|---|
| `ioc_to_sigma.json` | IOC → Sigma Rule | `cybersec` | Extract IOCs → MITRE map → generate Sigma rule |
| `cve_triage.json` | CVE Triage | `cybersec` | CVE lookup → exploitability analysis → remediation plan |
| `ir_triage.json` | IR Triage | `ir` | Alert intake → IOC extraction → SIEM queries → containment |
| `mitre_map.json` | MITRE Mapper | `cybersec` | TTP → ATT&CK techniques → detection plan |
| `recon_passive.json` | Passive Recon | `bugbounty` | OSINT-only recon for authorized bug bounty targets |

## Creating Custom Skills

1. Create a `.json` file in `Shared/skills/custom/` following the schema above
2. Skills appear automatically in the chat UI Skills panel on next launch
3. No restart required — skills are hot-loaded at session start

## Variable Reference

| Variable | Value |
|---|---|
| `{{input}}` | The user's input text or first message to the skill |
| `{{input_file}}` | Path to a file if one was attached |
| `{{timestamp}}` | ISO timestamp at skill execution time |
| `{{session_id}}` | Current chat session ID |
| `{{profile}}` | Active security profile ID |
| `{{output_var}}` | Value of any previously declared output variable |
