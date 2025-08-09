#!/usr/bin/env python3
"""Тест YouTube автоплея с новой функцией try_start_audio"""

import subprocess
import os

if __name__ == "__main__":
    print("🧪 Тестирование YouTube автоплея...")
    
    # Тест 1: YouTube видео без auto-play флага
    print("\n📋 Тест 1 - YouTube без auto-play:")
    cmd1 = [
        "c:\\Users\\user\\Desktop\\Open Interpreter\\.venv\\Scripts\\python.exe",
        "tools/browser.py",
        "--open", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "--duration", "8"
    ]
    
    try:
        result1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=15)
        print(f"  Код возврата: {result1.returncode}")
        print(f"  Вывод: {result1.stdout[:200]}...")
        if result1.stderr:
            print(f"  Ошибки: {result1.stderr[:200]}...")
    except subprocess.TimeoutExpired:
        print("  TIMEOUT: тест превысил лимит времени")
    except Exception as e:
        print(f"  ОШИБКА: {e}")
    
    # Тест 2: YouTube видео с auto-play флагом
    print("\n📋 Тест 2 - YouTube с --auto-play:")
    cmd2 = [
        "c:\\Users\\user\\Desktop\\Open Interpreter\\.venv\\Scripts\\python.exe", 
        "tools/browser.py",
        "--open", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "--auto-play",
        "--duration", "8"
    ]
    
    try:
        result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=15)
        print(f"  Код возврата: {result2.returncode}")
        print(f"  Вывод: {result2.stdout[:200]}...")
        if result2.stderr:
            print(f"  Ошибки: {result2.stderr[:200]}...")
    except subprocess.TimeoutExpired:
        print("  TIMEOUT: тест превысил лимит времени")
    except Exception as e:
        print(f"  ОШИБКА: {e}")
    
    print("\n✅ Тестирование автоплея завершено!")
