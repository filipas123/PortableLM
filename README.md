# PortableLM

Production-grade cybersecurity platform with multi-provider AI gateway, MCP server, 6-agent incident response ecosystem, SIEM/EDR integration, SOAR automation, and cyber range testing lab.

## Features

- **Multi-Provider AI:** Venice, KiloCode, Anthropic, OpenAI, Local Ollama
- **MCP Server:** Tool execution, sandboxing, audit logging
- **6-Agent Ecosystem:** Triage, Detection Engineer, Remediation, Threat Intel, IR Coordinator, Router
- **Real SIEM Integration:** Splunk, Elasticsearch, Microsoft Sentinel
- **Real EDR Integration:** CrowdStrike Falcon, Microsoft Defender XDR, SentinelOne
- **SOAR Automation:** Playbook execution, runbook automation, approval gates
- **Detection Lab:** Sigma rule validation, C2 beacon detection, attack pattern generation
- **Enterprise Deployment:** Docker Compose, Kubernetes, Terraform

## Quick Start

```bash
docker-compose up -d
```

Access dashboard: http://localhost:8080

## Documentation

- [Architecture](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT.md)
- [API Reference](API.md)
