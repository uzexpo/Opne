#!/usr/bin/env python3
"""Простой тест run_tool функции напрямую"""

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
    print("🧪 Тестирование run_tool напрямую...")
    
    # Тест 1: простая команда
    result1 = run_tool(["cmd", "/c", "echo Hello World"])
    print("\n📋 Тест 1 - echo:")
    if "error" in result1:
        print(f"  error: {result1['error']}")
    else:
        print(f"  ok: {result1['ok']}")
        print(f"  rc: {result1['rc']}")
        print(f"  out: {result1['out'][:100]}...")
        print(f"  err: {result1['err'][:100]}...")
    print(f"  cmd: {result1['cmd']}")
    
    # Тест 2: команда с ошибкой
    result2 = run_tool(["ping", "nonexistent.invalid.domain", "-n", "1"])
    print("\n📋 Тест 2 - ping несуществующего домена:")
    if "error" in result2:
        print(f"  error: {result2['error']}")
    else:
        print(f"  ok: {result2['ok']}")
        print(f"  rc: {result2['rc']}")
        print(f"  out: {result2['out'][:100]}...")
        print(f"  err: {result2['err'][:100]}...")
    print(f"  cmd: {result2['cmd']}")
    
    print("\n✅ Все тесты run_tool завершены!")
