#!/usr/bin/env python3
"""Тест audio.play через run_tool"""

import os
import sys
import subprocess

def run_tool(cmd: list[str], timeout: int = 120):
    """Универсальный запуск инструментов с расширенным логированием"""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "ok": proc.returncode == 0,
            "rc": proc.returncode,
            "out": proc.stdout[-2000:] if proc.stdout else "",  # хвост логов
            "err": proc.stderr[-2000:] if proc.stderr else "",
            "cmd": cmd
        }
    except subprocess.TimeoutExpired as e:
        return {
            "ok": False, 
            "timeout": True, 
            "out": e.stdout[-2000:] if e.stdout else "", 
            "err": e.stderr[-2000:] if e.stderr else "", 
            "cmd": cmd
        }
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}", "cmd": cmd}

if __name__ == "__main__":
    print("🧪 Тестирование audio.play через run_tool...")
    
    # Путь к Python из виртуального окружения
    VENV_PYTHON = r"c:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe"
    
    # Тест audio.play
    result = run_tool([
        VENV_PYTHON, 
        os.path.abspath("tools/audio.py"), 
        "--source", "https://samplelib.com/lib/preview/mp3/sample-3s.mp3", 
        "--volume", "70"
    ])
    
    print("\n📋 Результат audio.play:")
    if "error" in result:
        print(f"  error: {result['error']}")
    else:
        print(f"  ok: {result['ok']}")
        print(f"  rc: {result['rc']}")
        print(f"  out: {result['out']}")
        print(f"  err: {result['err']}")
    print(f"  cmd: {result['cmd']}")
    
    print("\n✅ Тест audio.play завершен!")
