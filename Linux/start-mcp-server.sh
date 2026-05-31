#!/bin/bash
set -e
echo "Starting PortableLM MCP Server (Port 3334)..."
cd "$(dirname "$0")"
cd ../Shared
python3 mcp/server.py --port 3334
