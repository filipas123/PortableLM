@echo off
title Portable AI - Fast Web Chat
color 0B

echo ===================================================
echo     Portable AI - Fast Web Chat Mode
echo ===================================================
echo.
echo  Launches the AI engine + browser chat UI.
echo  All chats auto-save to the USB drive.
echo.

:: Set paths to USB Shared Folder
set "OLLAMA_MODELS=%~dp0..\Shared\models\ollama_data"
set "OLLAMA_ORIGINS=*"
set "OLLAMA_HOST=127.0.0.1:11434"

:: GPU acceleration - push all layers to GPU (RTX/CUDA)
set "OLLAMA_GPU_LAYERS=999"
set "OLLAMA_NUM_PARALLEL=4"
set "OLLAMA_FLASH_ATTENTION=1"
set "CUDA_VISIBLE_DEVICES=0"

:: -------------------------------------------------------
:: Find Python: prefer portable USB copy, then system
:: -------------------------------------------------------
set "PYTHON_CMD="

:: Check for portable Python bundled on USB
if exist "%~dp0..\Shared\python\python.exe" (
    set "PYTHON_CMD=%~dp0..\Shared\python\python.exe"
    echo [OK] Using portable Python from USB drive.
    goto :PythonReady
)

:: Check for system-installed Python
python --version >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
    echo [OK] Using system Python.
    goto :PythonReady
)

:: Python not found anywhere
echo ===================================================
echo  ERROR: Python not found!
echo ===================================================
echo.
echo  Downloading portable Python to USB drive...
echo  (This only happens once, ~11MB download)
echo.

curl -L "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip" -o "%~dp0..\Shared\python-embed.zip"
if %errorlevel% neq 0 (
    echo Download failed. Please check your internet connection.
    pause
    exit
)

echo Extracting...
powershell -Command "Expand-Archive -Path '%~dp0..\Shared\python-embed.zip' -DestinationPath '%~dp0..\Shared\python' -Force"
del "%~dp0..\Shared\python-embed.zip" >nul 2>&1

if exist "%~dp0..\Shared\python\python.exe" (
    set "PYTHON_CMD=%~dp0..\Shared\python\python.exe"
    echo [OK] Portable Python installed on USB successfully!
) else (
    echo Failed to extract Python. Please try again.
    pause
    exit
)

:: -------------------------------------------------------
:: Run Mode Selection
:: -------------------------------------------------------
:PythonReady
echo.
echo ===================================================
echo  Run Mode
echo ===================================================
echo.
echo  [1] Local AI  (Ollama - uses your GPU/CPU)
echo  [2] Venice API (Cloud - access 671B+ models)
echo.
set /p RUN_MODE="  Your choice (1 or 2, default=1): "
if "%RUN_MODE%"=="" set RUN_MODE=1

if "%RUN_MODE%"=="2" goto :VeniceMode

:: -------------------------------------------------------
:: LOCAL MODE - Start Ollama Engine
:: -------------------------------------------------------
:LocalMode
if not exist "%~dp0..\Shared\bin\ollama-windows.exe" (
    echo.
    echo ===================================================
    echo  ERROR: Ollama Engine Not Found!
    echo ===================================================
    echo.
    echo  It looks like the AI engine hasn't been set up yet.
    echo  Please double-click "install.bat" in the Windows
    echo  folder first to safely download the components!
    echo.
    pause
    exit
)

:: Check if Ollama is already running
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Ollama engine is already running!
    goto :StartLocalChat
)

echo Starting Ollama Engine (GPU-accelerated)...
start /b "" "%~dp0..\Shared\bin\ollama-windows.exe" serve

echo Waiting for engine to initialize...
:WaitLoop
timeout /t 1 /nobreak >nul
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 goto :WaitLoop
echo [OK] Engine is online!

:StartLocalChat
echo.
echo ===================================================
echo  LOCAL AI ENGINE RUNNING  (RTX GPU accelerated)
echo  Chat UI opening at: http://localhost:3333
echo  Close this window to shut down everything.
echo ===================================================
echo.

%PYTHON_CMD% "%~dp0..\Shared\chat_server.py"

echo Shutting down...
taskkill /f /im ollama-windows.exe >nul 2>&1
echo Done. Goodbye!
pause
exit

:: -------------------------------------------------------
:: VENICE MODE - Cloud AI
:: -------------------------------------------------------
:VeniceMode
echo.
echo ===================================================
echo  Venice API Mode
echo ===================================================
echo.
echo  Available models:
echo    llama-3.3-70b        (default, best all-round)
echo    deepseek-r1-671b     (best reasoning, very slow)
echo    mistral-31-24b       (fast, vision capable)
echo    nous-hermes-3-llama-3.1-70b  (uncensored)
echo    qwen-2.5-vl          (vision + multimodal)
echo.
set /p VENICE_API_KEY="  Paste your Venice API key: "
if "%VENICE_API_KEY%"=="" (
    echo  ERROR: No API key entered. Switching to Local mode.
    goto :LocalMode
)
set /p VENICE_MODEL_INPUT="  Model name (Enter for llama-3.3-70b): "
if "%VENICE_MODEL_INPUT%"=="" (
    set VENICE_MODEL=llama-3.3-70b
) else (
    set VENICE_MODEL=%VENICE_MODEL_INPUT%
)

echo.
echo ===================================================
echo  VENICE API MODE  (model: %VENICE_MODEL%)
echo  Chat UI opening at: http://localhost:3333
echo  Close this window to shut down.
echo ===================================================
echo.

%PYTHON_CMD% "%~dp0..\Shared\chat_server.py" --venice

echo Done. Goodbye!
pause
