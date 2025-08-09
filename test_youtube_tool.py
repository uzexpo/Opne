#!/usr/bin/env python3
"""Простой тест tool_call для YouTube"""

import os
import sys
from urllib.parse import urlparse

def run_tool(cmd: list[str], timeout: int = 120):
    """Универсальный запуск инструментов с расширенным логированием"""
    import subprocess
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10  # Короткий таймаут для теста
        )
        return {
            "ok": proc.returncode == 0,
            "rc": proc.returncode,
            "out": proc.stdout[-500:] if proc.stdout else "",
            "err": proc.stderr[-500:] if proc.stderr else "",
            "cmd": cmd
        }
    except subprocess.TimeoutExpired as e:
        return {
            "ok": False, 
            "timeout": True, 
            "out": e.stdout[-500:] if e.stdout else "", 
            "err": e.stderr[-500:] if e.stderr else "", 
            "cmd": cmd
        }
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}", "cmd": cmd}

def is_allowed_url(url: str) -> tuple[bool, str]:
    """Проверяет разрешен ли URL согласно allowlist доменов"""
    try:
        h = urlparse(url).hostname or ""
        h = h.lower()
        allow = set()
        p = os.path.abspath("config/allowed_hosts.txt")
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    s = line.strip().lower()
                    if s and not s.startswith("#"):
                        allow.add(s)
        return (h in allow or any(h.endswith("."+a) for a in allow), h)
    except Exception as e:
        return (False, f"ERR:{e}")

def _browser_open_safe(url, duration=10, auto_play=False):
    allowed, host = is_allowed_url(url)
    if not allowed:
        return {"ok": False, "error": "host_not_allowed", "host": host, "hint": "add host to config/allowed_hosts.txt"}
    
    PYTHON_EXE = "c:\\Users\\user\\Desktop\\Open Interpreter\\.venv\\Scripts\\python.exe"
    cmd = [PYTHON_EXE, os.path.abspath("tools/browser.py"), "--open", url, "--duration", str(duration)]
    
    if auto_play:
        cmd.append("--auto-play")
    
    return run_tool(cmd)

if __name__ == "__main__":
    print("🧪 Тестирование YouTube tool_call...")
    
    # Тест с --auto-play
    print("\n📋 Тест YouTube с auto_play=True:")
    result = _browser_open_safe("https://youtube.com/watch?v=dQw4w9WgXcQ", duration=5, auto_play=True)
    
    print(f"  ok: {result.get('ok')}")
    print(f"  rc: {result.get('rc')}")
    if result.get('timeout'):
        print(f"  timeout: {result.get('timeout')}")
    if result.get('out'):
        print(f"  out: {result.get('out')}")
    if result.get('err'):
        print(f"  err: {result.get('err')}")
    print(f"  cmd: {result.get('cmd')}")
    
    print("\n✅ Тест завершен!")
