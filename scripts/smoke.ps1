$env:OI_WS_PORT = $env:OI_WS_PORT -as [int]
if (!$env:OI_WS_PORT) { $env:OI_WS_PORT = 8765 }

# Старт сервера (если не запущен)
Write-Host "Ensure server is running on ws://localhost:$env:OI_WS_PORT"
# (здесь предполагаем, что сервер уже запущен вручную)

# Прогон теста
& "c:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe" ".\tests\smoke_tool_calls.py"
