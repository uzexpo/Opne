@echo off
echo 🚀 Запуск Open Interpreter Electron приложения...
echo.

cd /d "%~dp0"
echo 📁 Текущая директория: %CD%

echo.
echo 📦 Проверка зависимостей...
if not exist "node_modules" (
    echo 📥 Установка Node.js зависимостей...
    npm install
)

echo.
echo 🎯 Запуск Electron приложения...
echo.

npx electron main-simple.js

if errorlevel 1 (
    echo.
    echo ❌ Ошибка запуска приложения!
    echo.
    echo 🔧 Возможные решения:
    echo   1. Убедитесь, что Node.js установлен
    echo   2. Попробуйте запустить: npm install
    echo   3. Проверьте, что все файлы на месте
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Приложение закрыто
pause 