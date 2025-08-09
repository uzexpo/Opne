@echo off
for /f "tokens=5" %%p in ('netstat -ano ^| findstr :8787') do taskkill /PID %%p /F >NUL 2>&1
echo OK: browserd stopped (if running)
