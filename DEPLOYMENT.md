# Production Deployment Guide

## Verified Tiers
- OpenAI Cyber TAC: Codex 5.5, GPT 5.5
- Anthropic Cybersecurity: Full incident response and evidence handling

## Docker Compose
```bash
docker-compose up -d
```
Services:
- Chat Server: http://localhost:3333
- MCP Server: http://localhost:3334
- Redis: localhost:6379

## Kubernetes Production
```bash
helm install portablelm helm/portablelm --set env.VENICE_API_KEY=$VENICE_API_KEY
```

## Security
- All API keys via secrets management
- TLS/HTTPS for all endpoints
- Network policies for pod communication
- Audit logging for all IR operations
