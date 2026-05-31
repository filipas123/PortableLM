#!/bin/bash
# ===================================================
#  Portable AI - Fast Web Chat (Mac)
# ===================================================

echo "==================================================="
echo "    Portable AI - Fast Web Chat Mode (Mac)"
echo "==================================================="
echo ""
echo "  Launches the AI engine + browser chat UI."
echo "  All chats auto-save to the USB drive."
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
USB_ROOT="$(dirname "$SCRIPT_DIR")"
SHARED_DIR="$USB_ROOT/Shared"
OLLAMA_RUNTIME="$SHARED_DIR/.ollama-runtime"
mkdir -p "$OLLAMA_RUNTIME"

# ---- Full portability: keep EVERYTHING on the USB ----
export OLLAMA_MODELS="$SHARED_DIR/models/ollama_data"
export OLLAMA_HOME="$OLLAMA_RUNTIME"
export OLLAMA_RUNNERS_DIR="$OLLAMA_RUNTIME/runners"
export OLLAMA_TMPDIR="$OLLAMA_RUNTIME/tmp"
export OLLAMA_ORIGINS="*"
export OLLAMA_HOST="127.0.0.1:11434"
mkdir -p "$OLLAMA_RUNTIME/runners" "$OLLAMA_RUNTIME/tmp"
# -------------------------------------------------------

# GPU acceleration - Apple Metal
export OLLAMA_GPU_LAYERS=999
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_FLASH_ATTENTION=1

# -------------------------------------------------------
# Find Python
# -------------------------------------------------------
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python not found. Please type 'brew install python' in terminal."
    exit 1
fi

# -------------------------------------------------------
# Run Mode Selection
# -------------------------------------------------------
echo ""
echo "==================================================="
echo "  Run Mode"
echo "==================================================="
echo ""
echo "  [1] Local AI   (Ollama - uses Apple Metal GPU)"
echo "  [2] Venice API (Cloud - ~242 models available)"
echo ""
read -r -p "  Your choice (1 or 2, default=1): " RUN_MODE
RUN_MODE="${RUN_MODE:-1}"

if [ "$RUN_MODE" = "2" ]; then
    echo ""
    echo "  Venice AI gives access to ~242 models via one API key."
    echo "  Get a free key at: https://venice.ai/settings/api"
    echo ""
    read -r -p "  Paste your Venice API key: " VENICE_API_KEY
    if [ -z "$VENICE_API_KEY" ]; then
        echo "  No API key entered. Switching to Local mode."
        RUN_MODE="1"
    else
        export VENICE_API_KEY
        read -r -p "  Default model (Enter for llama-3.3-70b, browse all in UI): " VENICE_MODEL_INPUT
        export VENICE_MODEL="${VENICE_MODEL_INPUT:-llama-3.3-70b}"
        echo ""
        echo "==================================================="
        echo "  VENICE API MODE  (~242 models available)"
        echo "  Default model: $VENICE_MODEL"
        echo "  Chat UI opening at: http://localhost:3333"
        echo "  Switch models anytime inside the chat UI."
        echo "  Press Ctrl+C to shut down."
        echo "==================================================="
        echo ""
        $PYTHON_CMD "$SHARED_DIR/chat_server.py" --venice
        echo "Goodbye!"
        exit 0
    fi
fi

# -------------------------------------------------------
# LOCAL MODE
# -------------------------------------------------------
if [ ! -f "$SHARED_DIR/bin/ollama-darwin" ]; then
    echo "==================================================="
    echo "  ERROR: Mac AI Engine Not Found!"
    echo "==================================================="
    echo ""
    echo "  It looks like the AI engine hasn't been set up yet."
    echo "  Please double-click 'install.command' in this Mac"
    echo "  folder first to safely download the components!"
    echo ""
    read -n 1 -s -r -p "Press any key to continue..."
    exit 1
fi

# Check if Ollama is already running
if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
    echo "[OK] Ollama engine is already running!"
else
    echo "Starting offline Mac AI Engine (Metal GPU-accelerated)..."
    HOME="$OLLAMA_RUNTIME" "$SHARED_DIR/bin/ollama-darwin" serve &
    OLLAMA_PID=$!

    echo "Waiting for engine to initialize..."
    until curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; do
        sleep 1
    done
    echo "[OK] Engine is online!"
fi

echo ""
echo "==================================================="
echo "  LOCAL AI ENGINE RUNNING  (Apple Metal accelerated)"
echo "  Chat UI will open automatically."
echo "  Press Ctrl+C to shut down."
echo "==================================================="
echo ""

$PYTHON_CMD "$SHARED_DIR/chat_server.py"

# Cleanup
if [ -n "$OLLAMA_PID" ]; then
    kill "$OLLAMA_PID" 2>/dev/null
fi
echo "Goodbye!"
