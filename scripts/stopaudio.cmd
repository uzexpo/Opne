@echo off
taskkill /IM vlc.exe /F >NUL 2>&1
echo OK: VLC stopped (if running)
