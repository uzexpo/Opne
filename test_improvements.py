#!/usr/bin/env python3
"""
Тестирование улучшенных tool_call инструментов
"""
import os
import subprocess
import time

def test_audio_features():
    print("🎵 Тестирование аудио функций...")
    
    # Тест 1: Обычное воспроизведение
    print("\n1. Воспроизведение аудио...")
    result = subprocess.run([
        r"C:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        "tools/audio.py",
        "--source", "https://samplelib.com/lib/preview/mp3/sample-3s.mp3",
        "--volume", "70"
    ], capture_output=True, text=True)
    print(f"Результат: {result.stdout.strip()}")
    
    # Тест 2: Pause функция  
    print("\n2. Тест pause...")
    result = subprocess.run([
        r"C:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        "tools/audio.py",
        "--pause"
    ], capture_output=True, text=True)
    print(f"Результат: {result.stdout.strip()}")
    
    # Тест 3: Resume функция
    print("\n3. Тест resume...")
    result = subprocess.run([
        r"C:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        "tools/audio.py",
        "--resume"
    ], capture_output=True, text=True)
    print(f"Результат: {result.stdout.strip()}")

def test_browser_features():
    print("\n🌐 Тестирование браузер функций...")
    
    # Тест 1: Автоплей на YouTube
    print("\n1. YouTube автоплей...")
    result = subprocess.run([
        r"C:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe", 
        "tools/browser.py",
        "--open", "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "--auto-play",
        "--duration", "8"
    ], capture_output=True, text=True)
    print(f"Результат: {result.stdout.strip()}")

def test_paths():
    print("\n🔍 Проверка путей...")
    
    # Проверяем VLC
    print("1. VLC установка:")
    result = subprocess.run(["winget", "list", "vlc"], capture_output=True, text=True)
    if "VideoLAN.VLC" in result.stdout:
        print("✅ VLC установлен")
    else:
        print("❌ VLC не найден")
    
    # Проверяем python-vlc
    print("\n2. Python-VLC:")
    result = subprocess.run([
        r"C:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        "-c", "import vlc; print('✅ python-vlc работает')"
    ], capture_output=True, text=True)
    if "✅" in result.stdout:
        print("✅ python-vlc работает")
    else:
        print(f"❌ python-vlc ошибка: {result.stderr}")

if __name__ == "__main__":
    os.chdir(r"C:\Users\user\Desktop\Open Interpreter\open-interpreter")
    
    test_paths()
    test_audio_features() 
    test_browser_features()
    
    print("\n✅ Тестирование завершено!")
