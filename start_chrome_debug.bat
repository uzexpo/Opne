@echo off
echo 🚀 Запуск Chrome с поддержкой автоматизации...

REM Закрываем все процессы Chrome
taskkill /F /IM chrome.exe 2>nul

REM Ждем завершения процессов
timeout /t 2 /nobreak > nul

REM Создаем временную директорию для отладки
if not exist "C:\temp" mkdir "C:\temp"
if not exist "C:\temp\chrome_debug" mkdir "C:\temp\chrome_debug"

REM Запускаем Chrome с отладочным портом
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"

echo ✅ Chrome запущен с поддержкой автоматизации!
echo 📡 Отладочный порт: 127.0.0.1:9222
echo.
echo Теперь Open Interpreter может:
echo - Читать содержимое вкладок
echo - Управлять браузером
echo - Автоматизировать веб-действия
echo.
pause
