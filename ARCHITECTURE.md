# PortableLM Architecture

## Components

### Chat Server (Port 3333)
- Multi-provider AI routing
- Live model fetching
- Security profile injection

### MCP Server (Port 3334)
- Tool execution with sandboxing
- Permission checking
- Approval gates
- Audit logging

### Agent Ecosystem
- Router Agent → Routes queries
- Triage Agent → Incident classification
- Detection Engineer → Rule generation
- Remediation Agent → Fix planning
- Threat Intel Agent → MITRE mapping
- IR Coordinator → Orchestration

### SIEM Connectors
- Splunk
- Elasticsearch
- Microsoft Sentinel

### EDR Connectors
- CrowdStrike Falcon
- Microsoft Defender XDR
- SentinelOne
