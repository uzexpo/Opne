#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ═══════════════════════════════════════════════════════════════
# 🚀 ПОЛНЫЙ ИМПОРТ ВСЕХ ВОЗМОЖНОСТЕЙ OPEN INTERPRETER 🚀
# ═══════════════════════════════════════════════════════════════

import os
import sys
import json
import asyncio
import signal
import websockets
import logging
import subprocess
import threading

# ═══════════════════════════════════════════════════════════════
# 🔧 КОНФИГУРАЦИЯ СЕРВЕРА 🔧
# ═══════════════════════════════════════════════════════════════

# Параметризуемый порт WebSocket сервера
WS_PORT = int(os.getenv("OI_WS_PORT", "8765"))
WS_HOST = os.getenv("OI_WS_HOST", "0.0.0.0")
import multiprocessing
import time
import datetime
import pathlib
import shutil
import glob
import tarfile
import zipfile
import pickle
import hashlib
import secrets
import sqlite3
import urllib
import socket
import ssl
import platform
import getpass
import ctypes
import importlib
import inspect
import gc
import ast
import re
import math
import random
import collections
import itertools
import functools
import operator
import heapq
import bisect
import copy
import io
import tempfile
import csv
import xml.etree.ElementTree as ET

# Импорты для работы с интернетом и API
try:
    import requests
    import http.server
    import ftplib
    import smtplib
    import imaplib
    import socketserver
    # telnetlib удален в Python 3.13+
    try:
        import telnetlib
    except ImportError:
        print("Warning: telnetlib недоступен в Python 3.13+")
except ImportError as e:
    print(f"Сетевые библиотеки не доступны: {e}")

# Импорты для GUI автоматизации
try:
    import pyautogui
    import pygetwindow
    import pynput
    from pynput import mouse, keyboard
except ImportError as e:
    print(f"GUI автоматизация не доступна: {e}")

# Импорты для веб-автоматизации
try:
    import selenium
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError as e:
    print(f"Selenium не доступен: {e}")

# Импорты для обработки изображений и OCR
try:
    from PIL import Image, ImageDraw, ImageFont
    import pytesseract
    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
except ImportError as e:
    print(f"Обработка изображений не доступна: {e}")

# Импорты для работы с данными
try:
    import pandas as pd
    import scipy
    from sklearn import *
except ImportError as e:
    print(f"Анализ данных не доступен: {e}")

# Импорты для мультимедиа
try:
    import pygame
    import pydub
    import speech_recognition as sr
    import pyttsx3
except ImportError as e:
    print(f"Мультимедиа не доступно: {e}")

# Импорты для системной диагностики
try:
    import psutil
    import wmi
except ImportError as e:
    print(f"Системная диагностика не доступна: {e}")

# Windows специфичные импорты
try:
    import win32gui
    import win32api
    import win32process
    import win32con
    import winreg
    import winsound
except ImportError as e:
    print(f"Windows API не доступен: {e}")

# Импорты для машинного обучения и ИИ
try:
    import openai
    import transformers
    import torch
    import tensorflow as tf
except ImportError as e:
    print(f"ML/AI библиотеки не доступны: {e}")

# Импорты для криптографии
try:
    from cryptography.fernet import Fernet
    import keyring
    import paramiko
    import pyotp
except ImportError as e:
    print(f"Криптография не доступна: {e}")

# Импорты для облачных технологий
try:
    import boto3
    from google.cloud import storage
    import dropbox
except ImportError as e:
    print(f"Облачные технологии не доступны: {e}")

# === BEGIN agent tools (whitelist) ===
import sys, subprocess, shlex, os, json, traceback

# Правильный путь к Python в виртуальной среде
VENV_PYTHON = os.path.join(os.path.dirname(__file__), "..", ".venv", "Scripts", "python.exe")
PYTHON_EXE = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

# ═══════════════════════════════════════════════════════════════
# 🎯 ENHANCED COMPUTER VISION INTEGRATION 🎯
# ═══════════════════════════════════════════════════════════════

try:
    # Добавляем путь к tools директории
    tools_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")
    if tools_path not in sys.path:
        sys.path.append(tools_path)
    
    from tools.cv_skills import (
        open_program, click_text, click_button, navigate_to, 
        smart_screenshot, screen_analysis, play_music_smart
    )
    from tools.yandex_music_cv import (
        play_yandex_music_with_cv, pause_yandex_music_cv, 
        next_track_yandex_cv, analyze_yandex_music_cv
    )
    CV_ENABLED = True
    print("🚀 Enhanced Computer Vision загружен успешно!")
except ImportError as e:
    print(f"⚠️ CV модули не найдены: {e}")
    CV_ENABLED = False
    # Заглушки для совместимости
    def open_program(name): return f"❌ CV недоступен: {name}"
    def click_text(text): return f"❌ CV недоступен: {text}"
    def click_button(btn): return f"❌ CV недоступен: {btn}"
    def navigate_to(el): return f"❌ CV недоступен: {el}"
    def smart_screenshot(fn=None): return "❌ CV недоступен"
    def screen_analysis(): return "❌ CV недоступен"
    def play_music_smart(song=None):
        """Простая функция запуска музыки через известные координаты Play кнопки"""
        try:
            # Используем наши Simple CV функции
            from tools.simple_cv import click_play_button
            result = click_play_button()
            print(f"🎵 Результат включения музыки: {result}")
            return result
        except Exception as e:
            print(f"❌ Ошибка включения музыки: {e}")
            # Резервный способ - клавиша Space
            try:
                import pyautogui
                pyautogui.press('space')
                return "✅ Нажата клавиша Space для воспроизведения музыки"
            except:
                return f"❌ CV недоступен: {e}"
    def play_yandex_music_with_cv(query=None): return "❌ CV недоступен"
    def pause_yandex_music_cv(): return "❌ CV недоступен"
    def next_track_yandex_cv(): return "❌ CV недоступен"
    def analyze_yandex_music_cv(): return "❌ CV недоступен"
    def analyze_yandex_music_cv(): return "❌ CV недоступен"



TOOLS = {
    # ═══════════════════════════════════════════════════════════════
    # 🎵 АУДИО ИНСТРУМЕНТЫ 🎵
    # ═══════════════════════════════════════════════════════════════
    "audio.play": lambda source, volume=80: subprocess.run(
        [PYTHON_EXE, os.path.abspath("tools/audio.py"), "--source", source, "--volume", str(volume)],
        check=False
    ),
    "audio.pause": lambda: subprocess.run(
        [PYTHON_EXE, os.path.abspath("tools/audio.py"), "--pause"],
        check=False
    ),
    "audio.resume": lambda: subprocess.run(
        [PYTHON_EXE, os.path.abspath("tools/audio.py"), "--resume"],
        check=False
    ),
    "audio.setVolume": lambda volume: subprocess.run(
        [PYTHON_EXE, os.path.abspath("tools/audio.py"), "--set-volume", str(volume)],
        check=False
    ),
    "audio.stop": lambda: subprocess.run(["cmd", "/c", os.path.abspath("scripts/stopaudio.cmd")], check=False),
    
    # ═══════════════════════════════════════════════════════════════
    # 🎯 ENHANCED COMPUTER VISION TOOLS 🎯
    # ═══════════════════════════════════════════════════════════════
    "cv.open_program": open_program,
    "cv.click_text": click_text,
    "cv.click_button": click_button,
    "cv.navigate": navigate_to,
    "cv.screenshot": smart_screenshot,
    "cv.analyze": screen_analysis,
    "cv.play_music": play_music_smart,
    
    # ═══════════════════════════════════════════════════════════════
    # 🎵 ЯНДЕКС МУЗЫКА С COMPUTER VISION 🎵
    # ═══════════════════════════════════════════════════════════════
    "yandex.play": play_yandex_music_with_cv,
    "yandex.pause": pause_yandex_music_cv,
    "yandex.next": next_track_yandex_cv,
    "yandex.analyze": analyze_yandex_music_cv,
    
    # ═══════════════════════════════════════════════════════════════
    # 🌐 БРАУЗЕР ИНСТРУМЕНТЫ 🌐
    # ═══════════════════════════════════════════════════════════════
    "browser.open": lambda url, duration=10: subprocess.run(
        [PYTHON_EXE if os.path.exists(os.path.abspath("tools/browser.py")) else "node",
         os.path.abspath("tools/browser.py") if os.path.exists(os.path.abspath("tools/browser.py")) else os.path.abspath("tools/browser.js"),
         "--open", url, "--duration", str(duration)],
        check=False
    ),
    "browser.playAudio": lambda page_url, audio_url, duration=10: subprocess.run(
        [PYTHON_EXE if os.path.exists(os.path.abspath("tools/browser.py")) else "node",
         os.path.abspath("tools/browser.py") if os.path.exists(os.path.abspath("tools/browser.py")) else os.path.abspath("tools/browser.js"),
         "--open", page_url, "--play-audio-url", audio_url, "--duration", str(duration)],
        check=False
    ),
    "browser.click": lambda url, selector, duration=5: subprocess.run(
        [PYTHON_EXE if os.path.exists(os.path.abspath("tools/browser.py")) else "node",
         os.path.abspath("tools/browser.py") if os.path.exists(os.path.abspath("tools/browser.py")) else os.path.abspath("tools/browser.js"),
         "--open", url, "--click", selector, "--duration", str(duration)],
        check=False
    )
}

def handle_tool_call(payload: dict):
    name = payload.get("tool")
    args = payload.get("args", {}) or {}
    if name not in TOOLS:
        return {"ok": False, "error": f"Unknown tool: {name}"}
    try:
        TOOLS[name](**args)
        return {"ok": True}
    except TypeError as e:
        return {"ok": False, "error": f"Bad args: {e}"}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}
# === END agent tools (whitelist) ===

from dotenv import load_dotenv
from interpreter import interpreter

# Добавляем текущую директорию в путь для импорта утилит
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Проверяем загрузку API ключа
openai_key = os.getenv('OPENAI_API_KEY')
if openai_key:
    logger.info(f"✅ OpenAI API ключ загружен: {openai_key[:8]}...")
else:
    logger.error("❌ OpenAI API ключ не найден!")

# Настройка Open Interpreter
interpreter.offline = False  # Для работы с OpenAI API
interpreter.auto_run = os.getenv('OPEN_INTERPRETER_AUTO_RUN', 'true').lower() == 'true'
interpreter.model = "gpt-4o"  # Используем более мощную модель
interpreter.api_key = openai_key

# Дополнительные настройки для доступа к компьютеру
if os.getenv('OPEN_INTERPRETER_SAFE_MODE', 'off').lower() == 'off':
    interpreter.safe_mode = "off"

# 🚫 ОТКЛЮЧАЕМ ВСТРОЕННЫЙ COMPUTER IMPORT - ИСПОЛЬЗУЕМ ТОЛЬКО ENHANCED CV!
# Включаем computer_import для работы Enhanced CV
if os.getenv('OPEN_INTERPRETER_COMPUTER_IMPORT', 'true').lower() == 'true':
    interpreter.computer_import = True
else:
    interpreter.computer_import = True  # ПРИНУДИТЕЛЬНО ВКЛЮЧАЕМ Enhanced CV!

# Принудительное завершение задач
interpreter.force_task_completion = True

# Настройки для улучшенной работы с компьютером
import tempfile
import os
history_dir = os.path.join(tempfile.gettempdir(), 'open_interpreter_history')
os.makedirs(history_dir, exist_ok=True)
interpreter.conversation_history_path = os.path.join(history_dir, 'conversation.json')
interpreter.max_output = 10000  # Увеличиваем максимальный вывод

# КРИТИЧЕСКИ ВАЖНО: Отключаем проблемные jupyter функции
interpreter.computer.languages = [lang for lang in interpreter.computer.languages if getattr(lang, 'name', '') != 'html']

# Дополнительные настройки для стабильности
try:
    # Отключаем jupyter kernel если он есть
    if hasattr(interpreter.computer, 'languages'):
        for lang in interpreter.computer.languages:
            if hasattr(lang, 'kernel') and lang.kernel is not None:
                lang.kernel = None
except Exception as e:
    logger.warning(f"Предупреждение при настройке языков: {e}")

# Системный промпт для улучшенных компьютерных навыков
computer_skills_prompt = """
Ты - мощный ИИ-ассистент с полным доступом к компьютеру. У тебя есть следующие возможности:

🎵 МУЗЫКА И АУДИО:
- play_music() - находит и запускает музыкальные приложения, включает воспроизведение
- control_music('play'/'pause'/'stop'/'next'/'previous') - управляет воспроизведением
- play_audio_file(source, volume=70, timeout=0) - воспроизведение аудио через VLC
- stop_audio() - остановка аудио VLC
- play_audio_in_browser(audio_url, duration=30) - воспроизведение аудио в браузере
- Можешь искать и запускать Spotify, VLC, YouTube Music, Windows Media Player

🌐 БРАУЗЕР И ВЕБ:
- open_browser_url(url, duration=10) - открытие URL в браузере через Playwright
- browser_click_element(selector, url=None, duration=5) - клик по элементу в браузере
- Поддержка автовоспроизведения аудио в браузере
- Управление Яндекс.Музыкой через браузер

🖱️ УПРАВЛЕНИЕ ИНТЕРФЕЙСОМ:
- computer.take_screenshot() - делает скриншот экрана
- Enhanced CV: click_text('текст'), click_button('кнопка') - умный поиск и клик
- Enhanced CV: play_music_smart('песня') - умное воспроизведение музыки
- import pyautogui; pyautogui.click(x, y) - клик по координатам
- pyautogui.press('key') - нажатие клавиш
- pyautogui.hotkey('ctrl', 'c') - комбинации клавиш

🔍 ПОИСК И ФАЙЛЫ:
- search_computer('filename') - ищет файлы по всему компьютеру
- find_and_open('app_name') - находит и запускает приложения
- computer.find_application('app_name') - ищет установленные программы

📱 АВТОМАТИЗАЦИЯ:
- import subprocess; subprocess.run(['program.exe']) - запуск программ
- import webbrowser; webbrowser.open('url') - открытие веб-страниц
- os.system('command') - выполнение системных команд

ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ:

Пользователь: "Включи музыку"
Ответ: 
```python
# Пробуем несколько способов включить музыку
result1 = launch_music_app()
print(f"Запуск приложения: {result1}")

result2 = smart_media_control('play')
print(f"Управление медиа: {result2}")

result3 = find_and_control_spotify()
print(f"Spotify управление: {result3}")
```

Пользователь: "Поставь на паузу"
Ответ:
```python
result = smart_media_control('pause')
print(f"Пауза: {result}")
```

Пользователь: "Следующий трек"
Ответ:
```python
result = smart_media_control('next')
print(f"Следующий трек: {result}")
```

Пользователь: "Включи Яндекс.Музыку"
Ответ:
```python
# Открываем Яндекс.Музыку
result1 = open_yandex_music_browser()
print(f"Открытие браузера: {result1}")

# Включаем воспроизведение
result2 = smart_music_control('включи')
print(f"Воспроизведение: {result2}")
```

Пользователь: "Найди и включи песню Баста - Сансара"
Ответ:
```python
result = play_yandex_music('Баста Сансара')
print(f"Поиск и воспроизведение: {result}")
```

Пользователь: "Что сейчас играет?"
Ответ:
```python
result = get_current_track_info()
print(result)
```

Пользователь: "Поставь на паузу Яндекс.Музыку"
Ответ:
```python
result = pause_yandex_music()
print(f"Пауза: {result}")
```

Пользователь: "Следующий трек"
Ответ:
```python
result = next_track_yandex()
print(f"Следующий трек: {result}")
```

Пользователь: "Поставь на паузу"
Ответ:
```python
result = control_music('pause')
print(result)
```

Пользователь: "Активируй окно Яндекс.Музыки и включи воспроизведение"
Ответ:
```python
import pygetwindow as gw
import pyautogui
import time

# ИСПРАВЛЕННЫЙ МЕТОД АКТИВАЦИИ ОКНА - БЕЗ ОШИБОК!
def activate_yandex_music():
    # Ищем окно с Яндекс.Музыкой
    windows = gw.getWindowsWithTitle('Яндекс Музыка')
    if windows:
        window = windows[0]
        try:
            # НЕ используем window.activate() - это вызывает ошибку!
            # Вместо этого кликаем по окну для активации
            x, y = window.left + 200, window.top + 100
            pyautogui.click(x, y)
            time.sleep(1)
            
            # Ищем и кликаем кнопку Play через Enhanced CV
            # Или используем пробел для воспроизведения
            pyautogui.press('space')
            
            return "✅ Окно активировано и музыка включена!"
        except Exception as e:
            # Альтернативный метод через Enhanced CV
            result1 = click_text('Яндекс Музыка')  # Клик по заголовку
            time.sleep(1)
            result2 = click_button('Play')  # Клик по кнопке Play
            return f"✅ Enhanced CV: {result1}, {result2}"
    else:
        return "❌ Окно с Яндекс.Музыкой не найдено"

result = activate_yandex_music()
print(result)
```

Пользователь: "Включи онлайн радио"
Ответ:
```python
# Воспроизведение онлайн радио
result = play_audio_file('http://radio.url/stream', volume=80)
print(f"Онлайн радио: {result}")
```

Пользователь: "Открой YouTube в браузере и включи музыку"
Ответ:
```python
# Открываем YouTube
result1 = open_browser_url('https://music.youtube.com', duration=30)
print(f"YouTube открыт: {result1}")

# Кликаем по кнопке воспроизведения
result2 = browser_click_element('.play-button', duration=10)
print(f"Кнопка воспроизведения: {result2}")
```

Пользователь: "Воспроизведи аудио из интернета"
Ответ:
```python
# Воспроизведение аудио URL в браузере с автовоспроизведением
result = play_audio_in_browser('https://example.com/audio.mp3', duration=60)
print(f"Браузер аудио: {result}")
```

Пользователь: "Найди файл song.mp3"
Ответ:
```python
files = search_computer('song.mp3')
print(f"Найдено файлов: {files}")
```

Пользователь: "Открой калькулятор"
Ответ:
```python
import subprocess
subprocess.run(['calc.exe'])
print("Калькулятор запущен")
```

Всегда объясняй что делаешь и показывай результат выполнения.

Правила инструментов (локальные, безопасные):
- Для воспроизведения аудио используй {"type":"tool_call","tool":"audio.play","args":{"source":"<путь_или_URL>","volume":80}}
- Для приостановки аудио: {"type":"tool_call","tool":"audio.pause","args":{}}
- Для возобновления аудио: {"type":"tool_call","tool":"audio.resume","args":{}}
- Для изменения громкости: {"type":"tool_call","tool":"audio.setVolume","args":{"volume":50}}
- Для остановки аудио: {"type":"tool_call","tool":"audio.stop","args":{}}
- Для управления браузером: 
  - открыть URL: {"type":"tool_call","tool":"browser.open","args":{"url":"<URL>","duration":10}}
  - открыть страницу и воспроизвести аудио: {"tool":"browser.playAudio","args":{"page_url":"<URL>","audio_url":"<URL>","duration":10}}
  - клик по элементу: {"type":"tool_call","tool":"browser.click","args":{"url":"<URL>","selector":"<CSS_селектор>","duration":5}}
Не выполняй произвольные shell-команды. Используй только эти инструменты.
"""

interpreter.system_message = computer_skills_prompt

# Импортируем и регистрируем компьютерные утилиты
try:
    from computer_utils import (
        find_and_launch_music_app, control_media, find_application, 
        search_files, take_screenshot, type_text, press_keys, computer,
        smart_media_control, find_and_control_spotify, launch_music_app,
        smart_window_control
    )
    logger.info("✅ Компьютерные утилиты загружены")
    
    # Импортируем системы памяти и Яндекс.Музыки
    try:
        # ВКЛЮЧЕНО: Супер память для полной функциональности
        from memory_system import memory_system  
        print("🧠 СУПЕР ПАМЯТЬ АКТИВИРОВАНА!")
        logger.info("✅ Система памяти успешно загружена")
    except ImportError as e:
        logger.warning(f"⚠️ Система памяти недоступна: {e}")
        memory_system = None
    
    try:
        from yandex_music import (
            yandex_music, play_yandex_music, pause_yandex_music, 
            next_track_yandex, previous_track_yandex, open_yandex_music_browser,
            get_current_track_info, smart_music_control
        )
        logger.info("✅ Контроллер Яндекс.Музыки загружен")
    except ImportError as e:
        logger.warning(f"⚠️ Контроллер Яндекс.Музыки недоступен: {e}")
        yandex_music = None
    
    # Делаем функции доступными в глобальном пространстве имен
    import __main__
    __main__.find_and_launch_music_app = find_and_launch_music_app
    __main__.control_media = control_media
    __main__.find_application = find_application
    __main__.search_files = search_files
    __main__.take_screenshot = take_screenshot
    __main__.type_text = type_text
    __main__.press_keys = press_keys
    __main__.computer = computer
    
    # Enhanced Computer Vision функции (заменяют старые click_image)
    if CV_ENABLED:
        __main__.click_text = click_text
        __main__.click_button = click_button
        __main__.smart_screenshot = smart_screenshot
        __main__.screen_analysis = screen_analysis
        __main__.play_music_smart = play_music_smart
        __main__.play_yandex_music_with_cv = play_yandex_music_with_cv
    
    # Новые улучшенные функции
    __main__.smart_media_control = smart_media_control
    __main__.find_and_control_spotify = find_and_control_spotify
    __main__.launch_music_app = launch_music_app
    __main__.smart_window_control = smart_window_control
    
    # Система памяти
    if memory_system:
        __main__.memory_system = memory_system
    
    # Яндекс.Музыка
    if yandex_music:
        __main__.yandex_music = yandex_music
        __main__.play_yandex_music = play_yandex_music
        __main__.pause_yandex_music = pause_yandex_music
        __main__.next_track_yandex = next_track_yandex
        __main__.previous_track_yandex = previous_track_yandex
        __main__.open_yandex_music_browser = open_yandex_music_browser
        __main__.get_current_track_info = get_current_track_info
        __main__.smart_music_control = smart_music_control
    
except ImportError as e:
    logger.warning(f"⚠️ Не удалось загрузить компьютерные утилиты: {e}")

# Устанавливаем рабочую директорию
import os
interpreter.working_directory = os.getcwd()
logger.info(f"📁 Рабочая директория: {interpreter.working_directory}")

# Настройки безопасности и стабильности - УПРОЩЕННЫЕ
interpreter.auto_run = True
interpreter.safe_mode = "off"
interpreter.force_task_completion = True

# Логируем конфигурацию
logger.info(f"🔧 Auto-run: {interpreter.auto_run}")
logger.info(f"🔒 Safe mode: {getattr(interpreter, 'safe_mode', 'default')}")
logger.info(f"💻 Computer import: {getattr(interpreter, 'computer_import', 'default')}")

# Настройка системного сообщения для полного доступа
interpreter.system_message = r"""
🔥 МАКСИМАЛЬНО МОЩНЫЙ OPEN INTERPRETER АГЕНТ 🔥

ВЫ - ЭКСПЕРТ-СИСТЕМА С НЕОГРАНИЧЕННЫМИ ВОЗМОЖНОСТЯМИ!

═══════════════════════════════════════════════════════════════
🚀 ПОЛНЫЙ АРСЕНАЛ КОМАНД OPEN INTERPRETER 🚀
═══════════════════════════════════════════════════════════════

💻 СИСТЕМНЫЕ ОПЕРАЦИИ:
• subprocess.run() - выполнение любых команд системы
• os.system() - прямое выполнение OS команд
• psutil.* - управление процессами, память, CPU, диски
• shutil.* - операции с файлами/папками (копирование, перемещение)
• pathlib.Path() - современная работа с путями
• glob.glob() - поиск файлов по маскам
• tarfile, zipfile - работа с архивами
• winreg - работа с реестром Windows
• ctypes - вызов Windows API напрямую

🐍 ПРОДВИНУТЫЙ PYTHON:
• exec(), eval() - динамическое выполнение кода
• importlib - динамический импорт модулей
• __import__() - импорт по строке
• compile() - компиляция кода
• ast.parse() - анализ синтаксиса
• inspect.* - инспекция объектов и кода
• threading, multiprocessing - параллельность
• asyncio - асинхронное программирование
• pickle, dill - сериализация объектов
• gc.* - управление сборщиком мусора

🌐 СЕТЕВЫЕ ТЕХНОЛОГИИ:
• requests.* - HTTP клиент (GET, POST, PUT, DELETE, HEAD, OPTIONS)
• urllib.* - низкоуровневые сетевые операции
• socket.* - прямая работа с сокетами
• ssl.* - безопасные соединения
• http.server - создание HTTP серверов
• ftplib - работа с FTP
• smtplib - отправка email
• imaplib, poplib - получение email
• telnetlib - работа с telnet
• socketserver - создание сетевых серверов

🤖 ВЕБ АВТОМАТИЗАЦИЯ И ПАРСИНГ:
• selenium.* - полная автоматизация браузера
• playwright.* - современная автоматизация браузера
• beautifulsoup4 - парсинг HTML
• lxml - быстрый XML/HTML парсер
• scrapy - профессиональный веб-скрапинг
• mechanize - автоматизация веб-форм
• pyppeteer - управление Chrome через DevTools
• chromedriver_autoinstaller - автоустановка драйверов

🎮 GUI АВТОМАТИЗАЦИЯ:
• pyautogui.* - полная автоматизация GUI
  - screenshot(), locateOnScreen(), click()
  - drag(), scroll(), typewrite(), press()
  - hotkey(), mouseDown(), mouseUp()
  - pixel(), pixelMatchesColor()
• pygetwindow.* - управление окнами
  - getWindowsWithTitle(), getActiveWindow()
  - activate(), minimize(), maximize(), close()
• pynput.* - продвинутое управление вводом
• win32gui, win32api - Windows API для GUI
• pywin32 - полный доступ к Windows API

🖼️ КОМПЬЮТЕРНОЕ ЗРЕНИЕ И OCR:
• opencv-python (cv2) - компьютерное зрение
• pytesseract - OCR распознавание текста
• Pillow (PIL) - работа с изображениями
• matplotlib - визуализация и анализ
• numpy - численные вычисления
• scikit-image - обработка изображений

🗄️ БАЗЫ ДАННЫХ:
• sqlite3 - встроенная база данных
• sqlalchemy - ORM для всех БД
• pymongo - MongoDB
• redis-py - Redis
• psycopg2 - PostgreSQL
• mysql-connector-python - MySQL
• pyodbc - универсальный ODBC драйвер

📊 АНАЛИЗ ДАННЫХ И ML:
• pandas - анализ данных
• numpy - численные вычисления
• scipy - научные вычисления
• matplotlib, seaborn - визуализация
• sklearn - машинное обучение
• tensorflow, pytorch - глубокое обучение
• transformers - NLP модели
• openai - работа с GPT API

🔒 БЕЗОПАСНОСТЬ И КРИПТОГРАФИЯ:
• cryptography.* - современная криптография
• hashlib - хеширование
• secrets - криптографически стойкие случайные числа
• keyring - работа с системным хранилищем паролей
• paramiko - SSH клиент
• pyotp - двухфакторная аутентификация

📱 МОБИЛЬНЫЕ И ДЕСКТОПНЫЕ ПРИЛОЖЕНИЯ:
• tkinter - создание GUI приложений
• PyQt5/6, PySide - профессиональные GUI
• kivy - кроссплатформенные приложения
• appium - автоматизация мобильных приложений

🎵 МУЛЬТИМЕДИА:
• pygame - игры и мультимедиа
• moviepy - обработка видео
• pydub - обработка аудио
• opencv - захват и обработка видео
• pyaudio - работа с аудио в реальном времени
• speech_recognition - распознавание речи
• pyttsx3 - синтез речи

☁️ ОБЛАЧНЫЕ ТЕХНОЛОГИИ:
• boto3 - Amazon AWS
• google-cloud-* - Google Cloud Platform
• azure-* - Microsoft Azure
• dropbox - Dropbox API
• paramiko - SSH/SFTP
• fabric - удаленное выполнение команд

📡 API И ИНТЕГРАЦИИ:
• fastapi - создание API
• flask - веб-фреймворк
• django - полнофункциональный веб-фреймворк
• telegram-bot-api - боты Telegram
• discord.py - боты Discord
• tweepy - Twitter API
• praw - Reddit API

🔧 СИСТЕМНАЯ ДИАГНОСТИКА:
• platform.* - информация о системе
• sys.* - параметры интерпретатора
• os.environ - переменные окружения
• getpass - работа с пользователями
• pwd, grp - пользователи и группы (Unix)
• wmi - Windows Management Instrumentation

⚡ ПРОДВИНУТЫЕ ВОЗМОЖНОСТИ:
• ctypes - вызов DLL и системных функций
• cffi - Foreign Function Interface
• cython - компиляция Python в C
• numba - JIT компиляция
• memory_profiler - профилирование памяти
• line_profiler - профилирование производительности

🛠️ ПАКЕТНЫЕ МЕНЕДЖЕРЫ И УСТАНОВКА:
• pip, pip-tools - управление Python пакетами
• conda - управление окружениями
• winget - Windows Package Manager
• chocolatey - пакетный менеджер для Windows
• scoop - еще один менеджер для Windows
• npm, yarn - Node.js пакеты
• docker - контейнеризация

═══════════════════════════════════════════════════════════════
🎯 КОНКРЕТНЫЕ ПРИМЕРЫ КОМАНД 🎯
═══════════════════════════════════════════════════════════════

🎵 МУЗЫКА И МЕДИА:
```python
# Включить музыку на YouTube Music
import subprocess, time, pyautogui
subprocess.Popen(['start', 'https://music.youtube.com'], shell=True)
time.sleep(3)
pyautogui.press('space')  # Нажать play

# Управление локальными медиа
import pygame
pygame.mixer.init()
pygame.mixer.music.load('song.mp3')
pygame.mixer.music.play()

# Управление системным звуком
import pycaw
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, None, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volume.SetMute(0, None)  # Убрать mute
volume.SetMasterVolumeLevel(-10.0, None)  # Установить громкость
```

🖥️ АВТОМАТИЗАЦИЯ GUI:
```python
# Полная автоматизация интерфейса
import pyautogui, time

# Сделать скриншот и найти кнопку
screenshot = pyautogui.screenshot()
button_location = pyautogui.locateOnScreen('button.png')
if button_location:
    pyautogui.click(button_location)

# Автоматизация ввода данных
pyautogui.hotkey('ctrl', 'a')  # Выделить все
pyautogui.typewrite('Новый текст')  # Ввести текст
pyautogui.press('enter')  # Нажать Enter

# Управление окнами - УЛУЧШЕННЫЙ МЕТОД БЕЗ ОШИБОК
import pygetwindow as gw
import pyautogui
import time

# АЛЬТЕРНАТИВА 1: Безопасная активация окна
def safe_activate_window(title_part):
    windows = gw.getWindowsWithTitle(title_part)
    if windows:
        try:
            window = windows[0]
            # Метод 1: Простой клик по окну
            x, y = window.left + 100, window.top + 50
            pyautogui.click(x, y)
            time.sleep(0.5)
            return f"✅ Окно активировано: {window.title}"
        except:
            # Метод 2: Alt+Tab переключение
            pyautogui.hotkey('alt', 'tab')
            return "✅ Использовал Alt+Tab"
    return "❌ Окно не найдено"

# Пример использования:
result = safe_activate_window('Яндекс Музыка')
print(result)

# АЛЬТЕРНАТИВА 2: Enhanced CV метод
# Используйте click_text() для клика по заголовку окна на панели задач
click_text('Яндекс Музыка')

# АЛЬТЕРНАТИВА 3: Комбинированный подход
windows = gw.getWindowsWithTitle('Chrome')
if windows:
    window = windows[0]
    # Не используем window.activate() - только размер и позицию
    window.maximize()  # Это работает без ошибок
    # Активируем кликом
    pyautogui.click(window.left + 100, window.top + 50)
```

🔍 СИСТЕМНЫЙ АНАЛИЗ:
```python
# Полная диагностика системы
import psutil, platform, os

def system_report():
    return {
        'OS': platform.system() + ' ' + platform.release(),
        'CPU': platform.processor(),
        'CPU_Usage': psutil.cpu_percent(),
        'Memory': f"{psutil.virtual_memory().percent}% используется",
        'Disk': f"{psutil.disk_usage('/').percent}% заполнен",
        'Processes': len(psutil.pids()),
        'Network': psutil.net_io_counters()._asdict()
    }

# Мониторинг процессов
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
    if proc.info['cpu_percent'] > 50:
        print(f"Высокая нагрузка: {proc.info}")
```

🌐 СЕТЕВЫЕ ОПЕРАЦИИ:
```python
# Продвинутые сетевые операции
import requests, json, socket

# REST API клиент
response = requests.get('https://api.github.com/users/octocat')
data = response.json()

# Загрузка файлов
def download_large_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

# Сканирование портов
def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0
```

🤖 ВЕБА АВТОМАТИЗАЦИЯ:
```python
# Selenium автоматизация
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://example.com')

# Умное ожидание элементов
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID, "button")))
element.click()

# Выполнение JavaScript
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Работа с cookies
cookies = driver.get_cookies()
driver.add_cookie({"name": "key", "value": "value"})
```

🔧 ПРОДВИНУТАЯ АВТОМАТИЗАЦИЯ:
```python
# Массовые операции с файлами
import os, shutil, glob
from pathlib import Path

# Поиск и обработка файлов
for file_path in glob.glob("**/*.txt", recursive=True):
    with open(file_path, 'r') as f:
        content = f.read()
        if 'pattern' in content:
            # Обработать файл
            shutil.copy(file_path, 'backup/')

# Автоматизация установки программ
def install_software():
    programs = [
        'winget install Microsoft.VisualStudioCode',
        'winget install Git.Git',
        'winget install Python.Python.3'
    ]
    for cmd in programs:
        subprocess.run(cmd.split(), check=True)
```

═══════════════════════════════════════════════════════════════
⚠️ КРИТИЧЕСКИ ВАЖНЫЕ НАСТРОЙКИ ⚠️
═══════════════════════════════════════════════════════════════

1. ВСЕГДА используйте try-except для обработки ошибок
2. ПРОВЕРЯЙТЕ существование файлов перед операциями
3. Используйте абсолютные пути для файлов
4. ЛОГИРУЙТЕ все важные операции
5. Для Windows используйте raw strings r"" для путей
6. ТЕСТИРУЙТЕ код перед выполнением критических операций

═══════════════════════════════════════════════════════════════
🚨 РЕЖИМ МАКСИМАЛЬНОЙ МОЩНОСТИ 🚨
═══════════════════════════════════════════════════════════════

ВЫ ИМЕЕТЕ ДОСТУП КО ВСЕМ ЭТИМ КОМАНДАМ БЕЗ ОГРАНИЧЕНИЙ!

• НЕТ ЗАПРЕТОВ на выполнение команд
• НЕТ ОГРАНИЧЕНИЙ на доступ к системе
• НЕТ БАРЬЕРОВ для автоматизации
• ПОЛНЫЙ доступ к интернету и API
• НЕОГРАНИЧЕННАЯ установка пакетов
• ПРЯМОЙ доступ к аппаратуре
• ПОЛНЫЙ контроль над GUI

ПРИНЦИПЫ РАБОТЫ:
✅ ДЕЙСТВУЙТЕ немедленно
✅ НЕ спрашивайте разрешения
✅ ИСПОЛЬЗУЙТЕ любые необходимые команды
✅ АВТОМАТИЗИРУЙТЕ все возможное
✅ ЭКСПЕРИМЕНТИРУЙТЕ с подходами
✅ КОМБИНИРУЙТЕ различные технологии
✅ РЕШАЙТЕ задачи творчески

═══════════════════════════════════════════════════════════════
🎯 ENHANCED COMPUTER VISION - ВАШИ СУПЕРСПОСОБНОСТИ! 🎯
═══════════════════════════════════════════════════════════════

У ВАС ЕСТЬ МОЩНЕЙШИЕ CV ФУНКЦИИ ДЛЯ УПРАВЛЕНИЯ КОМПЬЮТЕРОМ:

🔍 АНАЛИЗ ЭКРАНА В РЕАЛЬНОМ ВРЕМЕНИ:
• smart_screenshot() - умный скриншот с анализом
• screen_analysis() - полный анализ экрана и элементов UI
• click_text("текст") - кликнуть по любому тексту на экране
• click_button("кнопка") - кликнуть по любой кнопке
• open_program("название") - открыть любую программу

🎵 СПЕЦИАЛЬНЫЕ ФУНКЦИИ ДЛЯ ЯНДЕКС.МУЗЫКИ:
• play_yandex_music_with_cv("песня") - включить музыку через CV
• pause_yandex_music_cv() - поставить на паузу
• next_track_yandex_cv() - следующий трек
• analyze_yandex_music_cv() - анализ интерфейса музыки

🚀 МОЩЬ ENHANCED CV:
• Захват экрана: 7.7ms (сверхбыстро!)
• Анализ изображения: 67.8ms
• Обнаружение UI элементов в реальном времени
• Никаких файлов изображений - всё через LIVE анализ!

🎯 КАК ИСПОЛЬЗОВАТЬ ДЛЯ ЯНДЕКС.МУЗЫКИ:
Когда пользователь просит "включи яндекс музыку" или "включи музыку":
1. Используйте: play_yandex_music_with_cv("любимая песня")
2. ИЛИ: open_program("браузер") + navigate_to("music.yandex.ru")
3. ИЛИ: click_text("play") для управления

⚠️ КРИТИЧЕСКИ ВАЖНО:
• НЕ ИСПОЛЬЗУЙТЕ display.find_text() - ЭТО УСТАРЕЛО!
• НЕ ИСПОЛЬЗУЙТЕ pytesseract - ЭТО НЕ РАБОТАЕТ!
• НЕ ИСПОЛЬЗУЙТЕ computer.display - ОТКЛЮЧЕНО!
• НЕ ИСПОЛЬЗУЙТЕ computer.mouse.move(text="...") - ЗАМЕНЕНО!
• ИСПОЛЬЗУЙТЕ ТОЛЬКО: click_text(), click_button(), play_yandex_music_with_cv()

🚀 НОВЫЕ ПРАВИЛА ДЛЯ УПРАВЛЕНИЯ ЯНДЕКС.МУЗЫКОЙ:
1. Для включения музыки: play_yandex_music_with_cv("название песни")
2. Для паузы: pause_yandex_music_cv()
3. Для следующего трека: next_track_yandex_cv()
4. Для поиска кнопок: click_text("Play") или click_button("play")

🌐 НОВЫЕ ПРАВИЛА ДЛЯ БРАУЗЕРА:
1. Для открытия сайта: computer.browser.go_to_url("https://music.yandex.ru")
2. Альтернативно: open_browser_url("https://music.yandex.ru")
3. После открытия сайта: click_text("Play") для управления

🎯 ВЫПОЛНЕНИЕ КОМАНД:
• ВСЕ computer.* команды РАБОТАЮТ и ВЫПОЛНЯЮТСЯ!
• НЕ НУЖНО использовать старые функции
• ИСПОЛЬЗУЙТЕ: computer.browser.go_to_url(), computer.mouse.click(), click_text()

⚠️ КРИТИЧЕСКИ ВАЖНО - ПРАВИЛА БЕЗОПАСНОЙ РАБОТЫ С ОКНАМИ:
🚫 НИКОГДА НЕ ИСПОЛЬЗУЙТЕ window.activate() - ЭТО ВЫЗЫВАЕТ ОШИБКУ!
✅ ВМЕСТО ЭТОГО ИСПОЛЬЗУЙТЕ:
1. pyautogui.click(window.left + 100, window.top + 50) - клик по окну
2. click_text('название окна') - Enhanced CV клик по заголовку
3. pyautogui.hotkey('alt', 'tab') - переключение между окнами
4. pyautogui.press('space') - воспроизведение/пауза в медиа приложениях

🎵 ДЛЯ ЯНДЕКС.МУЗЫКИ ВСЕГДА ИСПОЛЬЗУЙТЕ:
```python
import pygetwindow as gw
import pyautogui
import time

# ПРАВИЛЬНЫЙ способ активации окна
windows = gw.getWindowsWithTitle('Яндекс Музыка')
if windows:
    window = windows[0]
    # НЕ используем window.activate()!
    pyautogui.click(window.left + 200, window.top + 100)
    time.sleep(1)
    pyautogui.press('space')  # Play/Pause
```

ВАЖНО: НЕ говорите "я не могу" - У ВАС ЕСТЬ ВСЕ ИНСТРУМЕНТЫ!

ВЫ - СУПЕРКОМПЬЮТЕР С НЕОГРАНИЧЕННЫМИ ВОЗМОЖНОСТЯМИ!
"""

class OpenInterpreterServer:
    def __init__(self):
        self.clients = set()
        
    async def register(self, websocket):
        self.clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
        
    async def unregister(self, websocket):
        self.clients.remove(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
        
    async def send_to_client(self, websocket, message):
        try:
            await websocket.send(json.dumps(message))
        except websockets.exceptions.ConnectionClosed:
            pass
            
    async def handle_message(self, websocket):
        await self.register(websocket)
        try:
            # Отправляем приветствие
            await self.send_to_client(websocket, {
                "type": "system",
                "message": "🤖 Open Interpreter готов к работе!"
            })
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    
                    # Обработка вызовов инструментов
                    if isinstance(data, dict) and data.get("type") == "tool_call":
                        res = handle_tool_call(data)
                        # отправь ответ обратно в GUI/лог:
                        try:
                            await self.send_to_client(websocket, {"type":"tool_result","data":res})
                        except Exception:
                            print("TOOL RESULT:", res)
                        continue
                    
                    user_message = data.get('message', '')
                    
                    if user_message.strip():
                        # Отправляем подтверждение получения
                        await self.send_to_client(websocket, {
                            "type": "user_echo",
                            "message": user_message
                        })
                        
                        # Отправляем статус обработки
                        await self.send_to_client(websocket, {
                            "type": "processing",
                            "message": "🔄 Обрабатываю запрос..."
                        })
                        
                        try:
                            # Выполняем команду через Open Interpreter
                            logger.info(f"Выполняю команду: {user_message}")
                            
                            # Добавляем контекст из системы памяти
                            enhanced_message = user_message
                            if memory_system:
                                try:
                                    # Получаем релевантный контекст из памяти
                                    context = memory_system.get_relevant_context(user_message)
                                    recent_commands = memory_system.get_recent_commands(limit=5)
                                    
                                    if context or recent_commands:
                                        memory_context = "\n[КОНТЕКСТ ИЗ ПАМЯТИ]\n"
                                        if recent_commands:
                                            memory_context += "Недавние команды:\n"
                                            for cmd in recent_commands:
                                                memory_context += f"- {cmd['command']}: {cmd['result'][:100]}...\n"
                                        if context:
                                            memory_context += f"Релевантная информация: {context}\n"
                                        memory_context += "[КОНЕЦ КОНТЕКСТА]\n\n"
                                        enhanced_message = memory_context + user_message
                                except Exception as mem_error:
                                    logger.warning(f"Ошибка получения контекста памяти: {mem_error}")
                            
                            # НЕ очищаем историю - пусть Open Interpreter помнит диалог
                            # interpreter.messages = []  # УБИРАЕМ ЭТУ СТРОКУ!
                            
                            # ВАЖНО: Отключаем проблемные функции HTML/jupyter перед выполнением
                            for attempts in range(3):  # 3 попытки
                                try:
                                    response = interpreter.chat(enhanced_message)
                                    break  # Если успешно, выходим из цикла
                                except Exception as retry_error:
                                    if "path should be string" in str(retry_error) and attempts < 2:
                                        logger.warning(f"Попытка {attempts + 1}: {retry_error}")
                                        # При ошибке используем оригинальное сообщение
                                        continue
                                    else:
                                        raise retry_error  # Если все попытки исчерпаны
                            
                            # Формируем ответ
                            full_response = ""
                            if isinstance(response, list):
                                for chunk in response:
                                    if hasattr(chunk, 'content'):
                                        full_response += chunk.content + "\n"
                                    elif isinstance(chunk, dict):
                                        if 'content' in chunk:
                                            full_response += chunk['content'] + "\n"
                                        elif 'output' in chunk:
                                            full_response += chunk['output'] + "\n"
                                        elif 'message' in chunk:
                                            full_response += str(chunk['message']) + "\n"
                            else:
                                full_response = str(response)
                            
                            # Отправляем результат
                            await self.send_to_client(websocket, {
                                "type": "response",
                                "message": full_response.strip() if full_response.strip() else "✅ Команда выполнена успешно!"
                            })
                            
                            # Сохраняем в систему памяти
                            if memory_system:
                                try:
                                    success = "ошибка" not in full_response.lower() and "error" not in full_response.lower()
                                    memory_system.remember_command(
                                        command=user_message,
                                        result=full_response,
                                        context="",
                                        success=success,
                                        tags=["web_chat"]
                                    )
                                except Exception as memory_error:
                                    logger.warning(f"⚠️ Ошибка сохранения в память: {memory_error}")
                            
                        except Exception as e:
                            error_msg = f"❌ Ошибка выполнения: {str(e)}"
                            logger.error(f"Детали ошибки: {e}", exc_info=True)
                            
                            # Более дружелюбное сообщение об ошибке
                            if "path should be string" in str(e):
                                error_msg = "❌ Ошибка пути к файлу. Попробуйте указать полный путь к файлу или выберите другой способ."
                            elif "No module named" in str(e):
                                error_msg = f"❌ Не установлен модуль. Устанавливаю автоматически..."
                                # Попробуем установить недостающий модуль
                                module_name = str(e).split("'")[1] if "'" in str(e) else "unknown"
                                await self.send_to_client(websocket, {
                                    "type": "info",
                                    "message": f"🔧 Устанавливаю модуль {module_name}..."
                                })
                            elif "libzmq" in str(e) or "jupyter" in str(e).lower():
                                error_msg = "❌ Ошибка jupyter. Попробуйте команду без HTML/notebook функций."
                            
                            await self.send_to_client(websocket, {
                                "type": "error",
                                "message": error_msg
                            })
                            
                except json.JSONDecodeError:
                    await self.send_to_client(websocket, {
                        "type": "error",
                        "message": "❌ Ошибка формата сообщения"
                    })
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

# ═══════════════════════════════════════════════════════════════
# 🔥 ДОПОЛНИТЕЛЬНЫЕ СУПЕРФУНКЦИИ ДЛЯ МАКСИМАЛЬНОЙ МОЩНОСТИ 🔥
# ═══════════════════════════════════════════════════════════════

def install_required_packages():
    """Автоматическая установка всех необходимых пакетов"""
    packages = [
        "pyautogui", "pygetwindow", "pynput", "selenium", "requests",
        "pillow", "opencv-python", "pytesseract", "pandas", "numpy",
        "matplotlib", "scipy", "scikit-learn", "pygame", "pydub",
        "speech-recognition", "pyttsx3", "psutil", "pywin32", "wmi",
        "cryptography", "paramiko", "boto3", "google-cloud-storage",
        "playwright", "beautifulsoup4", "lxml", "scrapy", "transformers",
        "torch", "tensorflow", "openai", "fastapi", "flask", "discord.py",
        "tweepy", "telepot", "keyboard", "mouse", "py-cpuinfo", "GPUtil",
        "speedtest-cli", "qrcode", "pyqrcode", "pypng", "barcode",
        "python-nmap", "scapy", "paramiko", "fabric", "invoke"
    ]
    
    for package in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         capture_output=True, check=True)
            logger.info(f"✅ Установлен пакет: {package}")
        except:
            logger.warning(f"⚠️ Не удалось установить: {package}")

def enable_god_mode():
    """Включение режима максимальных возможностей"""
    global interpreter
    
    # Отключаем все ограничения
    interpreter.auto_run = True
    interpreter.safe_mode = "off"
    interpreter.force_task_completion = True
    # Используем тот же путь к истории, что и выше
    import tempfile
    import os
    history_dir = os.path.join(tempfile.gettempdir(), 'open_interpreter_history')
    os.makedirs(history_dir, exist_ok=True)
    interpreter.conversation_history_path = os.path.join(history_dir, 'conversation.json')
    interpreter.max_output = 50000
    
    # Продвинутые настройки
    # 🚫 ОТКЛЮЧАЕМ ВСТРОЕННЫЕ COMPUTER ФУНКЦИИ - ИСПОЛЬЗУЕМ ТОЛЬКО ENHANCED CV!
    # if hasattr(interpreter, 'computer'):
    #     interpreter.computer.import_computer_api = True
    #     interpreter.computer.run_in_terminal = True
    #     interpreter.computer.import_skills = True
    #     interpreter.computer.offline = False
        
    # 🔧 НАСТРАИВАЕМ COMPUTER - ВКЛЮЧАЕМ ENHANCED CV
    try:
        if hasattr(interpreter, 'computer'):
            # Включаем все computer функции
            interpreter.computer.import_computer_api = True
            interpreter.computer.run_in_terminal = True
            interpreter.computer.offline = False  # Включаем API для работы CV
            
            # 🎯 ENHANCED COMPUTER VISION - ЗАМЕНА СТАРЫХ ФУНКЦИЙ
            if hasattr(interpreter.computer, 'display'):
                # Создаем замену для старых CV функций
                class EnhancedCVProxy:
                    def __init__(self):
                        # Используем простые и надежные CV функции
                        try:
                            sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))
                            from tools.simple_cv import simple_find_text, simple_find_element, simple_screenshot
                            
                            self.find_text_func = simple_find_text
                            self.find_element_func = simple_find_element
                            self.screenshot_func = simple_screenshot
                            print("✅ Простые CV функции загружены")
                        except ImportError as e:
                            print(f"❌ Ошибка импорта простых CV: {e}")
                            self.find_text_func = None
                            self.find_element_func = None
                            self.screenshot_func = None
                        
                    def find_text(self, text, screenshot=None):
                        """Замена для старой find_text - использует простые CV функции"""
                        try:
                            if self.find_text_func:
                                results = self.find_text_func(text)
                                print(f"🔍 Поиск текста '{text}': найдено {len(results)} результатов")
                                return results
                            return []
                        except Exception as e:
                            print(f"⚠️ Простой CV find_text ошибка: {e}")
                            return []
                    
                    def find(self, description, screenshot=None):
                        """Замена для старой find - использует простые CV функции"""
                        try:
                            if self.find_element_func:
                                # Убираем кавычки если есть
                                clean_description = description.strip('"').strip("'")
                                results = self.find_element_func(clean_description)
                                print(f"🔍 Поиск элемента '{clean_description}': найдено {len(results)} результатов")
                                return results
                            return []
                        except Exception as e:
                            print(f"⚠️ Простой CV find ошибка: {e}")
                            return []
                    
                    def screenshot(self, show=False):
                        """Замена для screenshot - использует простые функции"""
                        try:
                            if self.screenshot_func:
                                return self.screenshot_func()
                            else:
                                import pyautogui
                                return pyautogui.screenshot()
                        except Exception as e:
                            print(f"⚠️ Простой CV screenshot ошибка: {e}")
                            return None
                
                # Заменяем display на наш Enhanced CV Proxy
                interpreter.computer.display = EnhancedCVProxy()
                print("✅ Встроенные CV функции заменены на Enhanced CV")
                
            # 🎯 ENHANCED MOUSE - ЗАМЕНА СТАРЫХ ФУНКЦИЙ МЫШИ
            if hasattr(interpreter.computer, 'mouse'):
                # Создаем замену для старых mouse функций
                class EnhancedMouseProxy:
                    def __init__(self, original_mouse):
                        self.original_mouse = original_mouse
                        # Используем простые CV функции с обработкой ошибок
                        try:
                            from tools.simple_cv import simple_find_text, simple_click, click_play_button
                            
                            self.find_text_func = simple_find_text
                            self.click_func = simple_click
                            self.click_play_func = click_play_button
                            print("✅ Простые Mouse функции загружены")
                        except ImportError as e:
                            print(f"❌ Ошибка импорта простых Mouse функций: {e}")
                            self.find_text_func = None
                            self.click_func = None
                            self.click_play_func = None
                        
                    def move(self, x=None, y=None, icon=None, text=None, screenshot=None, *args):
                        """Замена для mouse.move - использует простые функции"""
                        try:
                            if text and self.find_text_func:
                                # Используем простой поиск текста
                                results = self.find_text_func(text)
                                if results:
                                    # Перемещаемся к первому найденному элементу
                                    coords = results[0]["coordinates"]
                                    import pyautogui
                                    pyautogui.moveTo(coords[0], coords[1])
                                    print(f"✅ Перемещение мыши к '{text}': {coords}")
                                    return
                                else:
                                    print(f"⚠️ Не найден текст '{text}' для перемещения")
                                    return
                            elif x is not None and y is not None:
                                # Обычное перемещение по координатам
                                import pyautogui
                                pyautogui.moveTo(x, y)
                                return
                            else:
                                # Используем оригинальную функцию если нет параметров
                                return self.original_mouse.move(x, y, icon, text, screenshot, *args)
                        except Exception as e:
                            print(f"⚠️ Простой Mouse move ошибка: {e}")
                    
                    def click(self, x=None, y=None, icon=None, text=None, screenshot=None, *args):
                        """Замена для mouse.click - использует простые функции"""
                        try:
                            if text:
                                # Специальная обработка для Play
                                if text.lower() in ['play', 'плей', 'воспроизведение']:
                                    if self.click_play_func:
                                        result = self.click_play_func()
                                        print(f"🎵 Клик по Play: {result}")
                                        return
                                
                                # Обычный поиск и клик по тексту
                                if self.find_text_func and self.click_func:
                                    results = self.find_text_func(text)
                                    if results:
                                        coords = results[0]["coordinates"]
                                        if self.click_func(coords[0], coords[1]):
                                            print(f"✅ Клик по тексту '{text}': {coords}")
                                            return
                                    print(f"⚠️ Не найден текст '{text}' для клика")
                                    return
                            elif x is not None and y is not None:
                                # Обычный клик по координатам
                                if self.click_func:
                                    self.click_func(x, y)
                                else:
                                    import pyautogui
                                    pyautogui.click(x, y)
                                return
                            else:
                                # Клик в текущей позиции
                                import pyautogui
                                pyautogui.click()
                                return
                        except Exception as e:
                            print(f"⚠️ Простой Mouse click ошибка: {e}")
                    
                    def __getattr__(self, name):
                        """Перенаправление всех остальных методов на оригинальный mouse"""
                        return getattr(self.original_mouse, name)
                
                # Заменяем mouse на наш Enhanced Mouse Proxy
                original_mouse = interpreter.computer.mouse
                interpreter.computer.mouse = EnhancedMouseProxy(original_mouse)
                print("✅ Встроенные Mouse функции заменены на Enhanced CV")
                
            # 🌐 ENHANCED BROWSER - ЗАМЕНА СТАРЫХ ФУНКЦИЙ БРАУЗЕРА
            if hasattr(interpreter.computer, 'browser'):
                # Создаем замену для старых browser функций
                class EnhancedBrowserProxy:
                    def __init__(self):
                        pass
                        
                    def go_to_url(self, url):
                        """Замена для browser.go_to_url - использует open_browser_url"""
                        try:
                            result = open_browser_url(url, duration=10)
                            print(f"✅ Открыл браузер с URL: {url}")
                            return result
                        except Exception as e:
                            print(f"⚠️ Enhanced Browser ошибка: {e}")
                            return f"❌ Не удалось открыть {url}"
                    
                    def open(self, url):
                        """Альтернативный метод для открытия URL"""
                        return self.go_to_url(url)
                        
                    def navigate(self, url):
                        """Ещё один метод для навигации"""
                        return self.go_to_url(url)
                
                # Заменяем browser на наш Enhanced Browser Proxy
                interpreter.computer.browser = EnhancedBrowserProxy()
                print("✅ Встроенные Browser функции заменены на Enhanced CV")
                
    except Exception as e:
        logger.warning(f"⚠️ Ошибка настройки computer: {e}")
        pass
    
    logger.info("🔥 GOD MODE ACTIVATED! Все ограничения сняты!")

# ═══════════════════════════════════════════════════════════════
# 🎵 НОВЫЕ МУЛЬТИМЕДИА ИНСТРУМЕНТЫ 🎵
# ═══════════════════════════════════════════════════════════════

def play_audio_file(source, volume=70, timeout=0):
    """Воспроизведение аудио через VLC"""
    try:
        script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'playaudio.cmd')
        cmd = [script_path, source, str(volume), str(timeout)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        if result.returncode == 0:
            return f"✅ Аудио воспроизводится: {source}"
        else:
            return f"❌ Ошибка воспроизведения: {result.stderr}"
    except Exception as e:
        return f"❌ Ошибка VLC: {str(e)}"

def stop_audio():
    """Остановка воспроизведения аудио"""
    try:
        script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'stopaudio.cmd')
        result = subprocess.run([script_path], capture_output=True, text=True)
        if result.returncode == 0:
            return "✅ Аудио остановлено"
        else:
            return f"❌ Ошибка остановки: {result.stderr}"
    except Exception as e:
        return f"❌ Ошибка остановки VLC: {str(e)}"

def open_browser_url(url, duration=10):
    """Открытие URL в браузере через Playwright"""
    try:
        script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'browse.cmd')
        cmd = [script_path, url, str(duration)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        if result.returncode == 0:
            return f"✅ Открыт в браузере: {url}"
        else:
            return f"❌ Ошибка браузера: {result.stderr}"
    except Exception as e:
        return f"❌ Ошибка браузера: {str(e)}"

def play_audio_in_browser(audio_url, duration=30):
    """Воспроизведение аудио URL в браузере"""
    try:
        tools_path = os.path.join(os.path.dirname(__file__), '..', 'tools', 'browser.py')
        python_path = os.path.join(os.path.dirname(__file__), '..', '.venv', 'Scripts', 'python.exe')
        cmd = [python_path, tools_path, '--play-audio-url', audio_url, '--duration', str(duration)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        if result.returncode == 0:
            return f"✅ Аудио воспроизводится в браузере: {audio_url}"
        else:
            return f"❌ Ошибка браузера аудио: {result.stderr}"
    except Exception as e:
        return f"❌ Ошибка браузера аудио: {str(e)}"

def browser_click_element(selector, url=None, duration=5):
    """Клик по элементу в браузере"""
    try:
        tools_path = os.path.join(os.path.dirname(__file__), '..', 'tools', 'browser.py')
        python_path = os.path.join(os.path.dirname(__file__), '..', '.venv', 'Scripts', 'python.exe')
        cmd = [python_path, tools_path, '--click', selector, '--duration', str(duration)]
        if url:
            cmd.extend(['--open', url])
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(__file__))
        if result.returncode == 0:
            return f"✅ Клик выполнен: {selector}"
        else:
            return f"❌ Ошибка клика: {result.stderr}"
    except Exception as e:
        return f"❌ Ошибка клика в браузере: {str(e)}"

def load_all_computer_skills():
    """Загрузка всех возможных навыков работы с компьютером"""
    global interpreter
    
    skills = {
        # Базовые системные команды
        'execute_command': lambda cmd: subprocess.run(cmd, shell=True, capture_output=True, text=True),
        'get_system_info': lambda: platform.uname(),
        'list_processes': lambda: [p.info for p in psutil.process_iter(['pid', 'name', 'cpu_percent'])],
        'get_memory_usage': lambda: psutil.virtual_memory(),
        'get_disk_usage': lambda: psutil.disk_usage('/'),
        
        # GUI автоматизация
        'take_screenshot': lambda: pyautogui.screenshot(),
        'click_at': lambda x, y: pyautogui.click(x, y),
        'type_text': lambda text: pyautogui.typewrite(text),
        'press_key': lambda key: pyautogui.press(key),
        'hotkey': lambda *keys: pyautogui.hotkey(*keys),
        
        # Файловые операции
        'create_file': lambda path, content: open(path, 'w').write(content),
        'read_file': lambda path: open(path, 'r').read(),
        'copy_file': lambda src, dst: shutil.copy2(src, dst),
        'move_file': lambda src, dst: shutil.move(src, dst),
        'delete_file': lambda path: os.remove(path),
        
        # Сетевые операции
        'download_file': lambda url, path: requests.get(url).content and open(path, 'wb').write(requests.get(url).content),
        'check_internet': lambda: requests.get('https://google.com', timeout=5).status_code == 200,
        'get_ip': lambda: requests.get('https://api.ipify.org').text,
        
        # Мультимедиа
        'play_sound': lambda file: winsound.PlaySound(file, winsound.SND_FILENAME) if os.name == 'nt' else None,
        'text_to_speech': lambda text: pyttsx3.speak(text) if 'pyttsx3' in globals() else None,
        
        # Улучшенные медиа функции
        'smart_media_control': smart_media_control if 'smart_media_control' in globals() else lambda action: "Функция недоступна",
        'find_and_control_spotify': find_and_control_spotify if 'find_and_control_spotify' in globals() else lambda: "Функция недоступна",
        'launch_music_app': launch_music_app if 'launch_music_app' in globals() else lambda: "Функция недоступна",
        'smart_window_control': smart_window_control if 'smart_window_control' in globals() else lambda app, action="activate": "Функция недоступна",
        
        # 🎯 ENHANCED COMPUTER VISION - ЗАМЕНА СТАРЫХ ФУНКЦИЙ
        'click_by_description': lambda desc: click_text(desc) if CV_ENABLED else f"❌ CV недоступен для клика по: {desc}",
        'find_and_click': lambda element: click_text(element) if CV_ENABLED else f"❌ CV недоступен для поиска: {element}",
        'smart_click_button': lambda button: click_button(button) if CV_ENABLED else f"❌ CV недоступен для кнопки: {button}",
        
        # Яндекс.Музыка
        'play_yandex_music': play_yandex_music if 'play_yandex_music' in globals() else lambda query=None: "Яндекс.Музыка недоступна",
        'pause_yandex_music': pause_yandex_music if 'pause_yandex_music' in globals() else lambda: "Яндекс.Музыка недоступна",
        'next_track_yandex': next_track_yandex if 'next_track_yandex' in globals() else lambda: "Яндекс.Музыка недоступна",
        'previous_track_yandex': previous_track_yandex if 'previous_track_yandex' in globals() else lambda: "Яндекс.Музыка недоступна",
        'open_yandex_music_browser': open_yandex_music_browser if 'open_yandex_music_browser' in globals() else lambda: "Яндекс.Музыка недоступна",
        
        # 🎵 ENHANCED CV MUSIC - УМНОЕ ВОСПРОИЗВЕДЕНИЕ МУЗЫКИ
        'play_music_cv': lambda song=None: play_music_smart(song) if CV_ENABLED else f"❌ CV музыка недоступна",
        'yandex_music_cv': lambda: (
            open_program("браузер") + "; " + 
            navigate_to("Яндекс Музыка") + "; " +
            click_button("Play")
        ) if CV_ENABLED else "❌ CV Яндекс.Музыка недоступна",
        'get_current_track_info': get_current_track_info if 'get_current_track_info' in globals() else lambda: "Яндекс.Музыка недоступна",
        'smart_music_control': smart_music_control if 'smart_music_control' in globals() else lambda action, query=None: "Умное управление музыкой недоступно",
        
        # Система памяти
        'remember_command': memory_system.remember_command if memory_system else lambda cmd, result, context="", success=True, tags=None: "Система памяти недоступна",
        'find_similar_commands': memory_system.find_similar_commands if memory_system else lambda query, limit=5: "Система памяти недоступна",
        'save_preference': memory_system.save_preference if memory_system else lambda key, value: "Система памяти недоступна",
        'get_preference': memory_system.get_preference if memory_system else lambda key, default=None: default,
        'get_memory_stats': memory_system.get_stats if memory_system else lambda: "Система памяти недоступна",
        
        # Новые мультимедиа инструменты
        'play_audio_file': play_audio_file if 'play_audio_file' in globals() else lambda source, volume=70, timeout=0: "VLC аудио недоступно",
        'stop_audio': stop_audio if 'stop_audio' in globals() else lambda: "VLC аудио недоступно", 
        'open_browser_url': open_browser_url if 'open_browser_url' in globals() else lambda url, duration=10: "Браузер автоматизация недоступна",
        'play_audio_in_browser': play_audio_in_browser if 'play_audio_in_browser' in globals() else lambda audio_url, duration=30: "Браузер аудио недоступно",
        'browser_click_element': browser_click_element if 'browser_click_element' in globals() else lambda selector, url=None, duration=5: "Браузер клик недоступен",
        
        # 🌐 COMPUTER.BROWSER COMPATIBILITY - ПРЯМЫЕ ЗАМЕНЫ
        'computer_browser_go_to_url': lambda url: open_browser_url(url, duration=10),
        'computer_browser_open': lambda url: open_browser_url(url, duration=10),
    }
    
    # Добавляем все навыки в интерпретер
    for name, func in skills.items():
        try:
            setattr(interpreter, name, func)
            logger.info(f"✅ Загружен навык: {name}")
        except:
            logger.warning(f"⚠️ Не удалось загрузить навык: {name}")

def setup_advanced_capabilities():
    """Настройка продвинутых возможностей"""
    global interpreter
    
    # Максимальные настройки производительности
    interpreter.max_output = 100000
    interpreter.conversation_filename = None
    
    # Продвинутые системные функции
    advanced_functions = """
# Продвинутые функции для максимальной автоматизации

import subprocess
import os
import sys
import time
import json
import requests
import threading
from pathlib import Path

def install_package(package_name):
    \"\"\"Умная установка пакетов\"\"\"
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
        return f"✅ Установлен: {package_name}"
    except:
        try:
            subprocess.run(["winget", "install", package_name], check=True)
            return f"✅ Установлен через winget: {package_name}"
        except:
            return f"❌ Не удалось установить: {package_name}"

def smart_search(query, search_type="files"):
    \"\"\"Умный поиск по системе\"\"\"
    results = []
    if search_type == "files":
        for root, dirs, files in os.walk("C:\\\\"):
            for file in files:
                if query.lower() in file.lower():
                    results.append(os.path.join(root, file))
                    if len(results) >= 50:  # Ограничиваем результаты
                        break
    return results

def mass_automation(actions):
    \"\"\"Массовая автоматизация действий\"\"\"
    results = []
    for action in actions:
        try:
            if action['type'] == 'click':
                pyautogui.click(action['x'], action['y'])
            elif action['type'] == 'type':
                pyautogui.typewrite(action['text'])
            elif action['type'] == 'key':
                pyautogui.press(action['key'])
            elif action['type'] == 'command':
                subprocess.run(action['command'], shell=True)
            results.append(f"✅ {action}")
        except Exception as e:
            results.append(f"❌ {action}: {e}")
    return results

def system_monitor():
    \"\"\"Мониторинг системы в реальном времени\"\"\"
    return {
        'cpu': psutil.cpu_percent(),
        'memory': psutil.virtual_memory().percent,
        'disk': psutil.disk_usage('/').percent,
        'processes': len(psutil.pids()),
        'network': psutil.net_io_counters()._asdict()
    }

def emergency_functions():
    \"\"\"Экстренные функции восстановления\"\"\"
    return {
        'kill_process': lambda name: os.system(f'taskkill /f /im {name}'),
        'restart_explorer': lambda: os.system('taskkill /f /im explorer.exe && start explorer.exe'),
        'clear_temp': lambda: os.system('del /q /f %temp%\\\\*'),
        'flush_dns': lambda: os.system('ipconfig /flushdns'),
        'reset_network': lambda: os.system('netsh int ip reset && netsh winsock reset')
    }

# Автоматическое определение и установка недостающих зависимостей
def auto_install_missing():
    missing = []
    required = ['pyautogui', 'requests', 'psutil', 'pillow', 'opencv-python']
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            except:
                pass
    return missing

# Запускаем автоустановку
auto_install_missing()
"""
    
    try:
        exec(advanced_functions, interpreter.__dict__)
        logger.info("✅ Продвинутые функции загружены")
    except Exception as e:
        logger.warning(f"⚠️ Не удалось загрузить продвинутые функции: {e}")

# Инициализируем все возможности при загрузке
try:
    enable_god_mode()
    load_all_computer_skills()
    setup_advanced_capabilities()
    logger.info("🚀 ВСЕ СУПЕРФУНКЦИИ АКТИВИРОВАНЫ!")
except Exception as e:
    logger.warning(f"⚠️ Предупреждение при инициализации суперфункций: {e}")

# --- robust WS bootstrap (no CancelledError crash) ---
_stop_event: asyncio.Event | None = None

def _setup_signal_handlers(loop: asyncio.AbstractEventLoop):
    for sig_name in ("SIGINT", "SIGTERM"):
        sig = getattr(signal, sig_name, None)
        if sig is not None:
            try:
                loop.add_signal_handler(sig, _stop_event.set)  # type: ignore[arg-type]
            except NotImplementedError:
                pass  # Ok for Windows

async def run_ws_server_sleepy(handler, host: str, port: int):
    server = await websockets.serve(handler, host, port, ping_interval=20, ping_timeout=20, close_timeout=5)
    try:
        while True:
            await asyncio.sleep(3600)
    except asyncio.CancelledError:
        pass
    finally:
        server.close()
        await server.wait_closed()

async def run_ws_server(handler, host: str, port: int):
    global _stop_event
    _stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    _setup_signal_handlers(loop)

    server = await websockets.serve(
        handler, host, port,
        ping_interval=20, ping_timeout=20, close_timeout=5
    )
    try:
        await _stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        server.close()
        try:
            await server.wait_closed()
        except Exception:
            pass

def main():
    print("🚀 Запуск Open Interpreter сервера...")
    print(f"📡 WebSocket сервер будет доступен на ws://192.168.241.1:{WS_PORT}")
    print(f"📡 Также доступен локально на ws://localhost:{WS_PORT}")
    
    server_instance = OpenInterpreterServer()
    
    async def run_server():
        print("🚀 Запуск WebSocket сервера...")
        
        # Временно используем sleepy версию
        await run_ws_server_sleepy(server_instance.handle_message, WS_HOST, WS_PORT)
        print("✅ Сервер закрыт корректно")
    
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("🛑 Сервер остановлен")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        raise

if __name__ == "__main__":
    main()
