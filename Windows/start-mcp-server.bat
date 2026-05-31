@echo off
setlocal enabledelayedexpansion
echo Starting PortableLM MCP Server (Port 3334)...
cd /d "%~dp0.."
cd Shared
python mcp/server.py --port 3334
pause
