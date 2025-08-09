@echo off
echo 🚀 Запуск Open Interpreter Electron приложения...
echo.

echo 📦 Проверка зависимостей...
if not exist "node_modules" (
    echo 📥 Установка Node.js зависимостей...
    npm install
    if errorlevel 1 (
        echo ❌ Ошибка установки зависимостей!
        pause
        exit /b 1
    )
)

echo.
echo 🔧 Проверка Python зависимостей...
python -c "import websockets" 2>nul
if errorlevel 1 (
    echo 📥 Установка Python зависимостей...
    pip install websockets
    if errorlevel 1 (
        echo ❌ Ошибка установки Python зависимостей!
        pause
        exit /b 1
    )
)

echo.
echo 🎯 Запуск Electron приложения...
echo.
echo 📋 Возможности:
echo   • Автоматический запуск Python сервера
echo   • Современный веб-интерфейс
echo   • Управление сервером через GUI
echo   • Сохранение/загрузка чата
echo   • Быстрые команды
echo   • Лог сервера
echo.

echo ⏳ Запуск приложения...
npm start

if errorlevel 1 (
    echo.
    echo ❌ Ошибка запуска приложения!
    echo.
    echo 🔧 Возможные решения:
    echo   1. Убедитесь, что Node.js установлен
    echo   2. Убедитесь, что Python установлен
    echo   3. Проверьте, что все файлы на месте
    echo   4. Попробуйте запустить: npm install
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Приложение закрыто
pause 