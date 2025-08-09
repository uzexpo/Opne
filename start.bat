@echo off
echo 🚀 Запуск Open Interpreter Chat...
echo.

echo 📡 Запуск Python сервера...
start "Python Server" cmd /k "cd /d "%~dp0" && "C:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe" "C:\Users\user\Desktop\Open Interpreter\open-interpreter\server.py""

echo ⏳ Ожидание запуска сервера...
timeout /t 5 /nobreak > nul

echo 🖥️ Запуск Electron приложения...
cd /d "%~dp0"
npx electron .

pause
