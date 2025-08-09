@echo off
set PORT=%~1
if "%PORT%"=="" set PORT=8787
set BROWSERD_PORT=%PORT%
"C:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe" -m uvicorn tools.browser_service:app --host 127.0.0.1 --port %PORT%
