@echo off
set SRC=%~1
set VOL=%~2
if "%VOL%"=="" set VOL=80
"C:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe" "%~dp0..\tools\audio.py" --source "%SRC%" --volume %VOL%
