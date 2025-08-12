#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ═══════════════════════════════════════════════════════════════
# 🚀 ПОЛНЫЙ ИМПОРТ ВСЕХ ВОЗМОЖНОСТЕЙ OPEN INTERPRETER 🚀
# ═══════════════════════════════════════════════════════════════

import os
import sys
import json
import asyncio
import websockets
import logging
from logging.handlers import RotatingFileHandler
import subprocess
import threading
import shlex
from urllib.parse import urlparse
import requests

# ═══════════════════════════════════════════════════════════════
# �️ УНИВЕРСАЛЬНЫЙ РАННЕР ИНСТРУМЕНТОВ 🛠️
# ═══════════════════════════════════════════════════════════════

def run_tool(cmd: list[str], timeout: int = 120):
    """Универсальный запуск инструментов с расширенным логированием"""
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Санитация stderr - убираем безвредные предупреждения
        HARMLESS = ("Could not find platform independent libraries <prefix>",)
        err = (proc.stderr or "")
        for s in HARMLESS:
            err = err.replace(s, "")
        
        return {
            "ok": proc.returncode == 0,
            "rc": proc.returncode,
            "out": proc.stdout[-2000:] if proc.stdout else "",  # хвост логов
            "err": err[-2000:],
            "cmd": cmd
        }
    except subprocess.TimeoutExpired as e:
        # Санитация stderr для timeout случая
        HARMLESS = ("Could not find platform independent libraries <prefix>",)
        err = (e.stderr or "")
        for s in HARMLESS:
            err = err.replace(s, "")
            
        return {
            "ok": False, 
            "timeout": True, 
            "out": e.stdout[-2000:] if e.stdout else "", 
            "err": err[-2000:], 
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

# ═══════════════════════════════════════════════════════════════
# 📝 НАСТРОЙКА ЛОГИРОВАНИЯ С РОТАЦИЕЙ 📝
# ═══════════════════════════════════════════════════════════════

os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("agent")
logger.setLevel(logging.INFO)
fh = RotatingFileHandler("logs/agent.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8")
fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
fh.setFormatter(fmt)
logger.addHandler(fh)

# ═══════════════════════════════════════════════════════════════
# �🔧 КОНФИГУРАЦИЯ СЕРВЕРА 🔧
# ═══════════════════════════════════════════════════════════════

# Параметризуемый порт WebSocket сервера
WS_PORT = int(os.getenv("OI_WS_PORT", "8765"))
WS_HOST = os.getenv("OI_WS_HOST", "0.0.0.0")

# Конфигурация браузер-сервиса
BROWSERD_PORT = int(os.getenv("BROWSERD_PORT", "8787"))
BROWSERD_URL = f"http://127.0.0.1:{BROWSERD_PORT}"
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

# Функции-обертки с проверкой allowlist
def _browser_open_safe(url, duration=10, auto_play=False):
    allowed, host = is_allowed_url(url)
    if not allowed:
        return {"ok": False, "error": "host_not_allowed", "host": host, 
                "hint": "Домен не разрешен. Добавьте его в config/allowed_hosts.txt или получите подтверждение пользователя."}
    
    cmd = [PYTHON_EXE if os.path.exists(os.path.abspath("tools/browser.py")) else "node",
           os.path.abspath("tools/browser.py") if os.path.exists(os.path.abspath("tools/browser.py")) else os.path.abspath("tools/browser.js"),
           "--open", url, "--duration", str(duration)]
    
    if auto_play:
        cmd.append("--auto-play")
    
    return run_tool(cmd)

def _browser_play_audio_safe(page_url, audio_url, duration=10):
    allowed_page, host_page = is_allowed_url(page_url)
    allowed_audio, host_audio = is_allowed_url(audio_url)
    if not allowed_page:
        return {"ok": False, "error": "host_not_allowed", "host": host_page, "hint": "add host to config/allowed_hosts.txt"}
    if not allowed_audio:
        return {"ok": False, "error": "host_not_allowed", "host": host_audio, "hint": "add host to config/allowed_hosts.txt"}
    return run_tool(
        [PYTHON_EXE if os.path.exists(os.path.abspath("tools/browser.py")) else "node",
         os.path.abspath("tools/browser.py") if os.path.exists(os.path.abspath("tools/browser.py")) else os.path.abspath("tools/browser.js"),
         "--open", page_url, "--play-audio-url", audio_url, "--duration", str(duration)]
    )

def _browser_click_safe(url, selector, duration=5):
    allowed, host = is_allowed_url(url)
    if not allowed:
        return {"ok": False, "error": "host_not_allowed", "host": host, 
                "hint": "Домен не разрешен. Добавьте его в config/allowed_hosts.txt или получите подтверждение пользователя."}
    return run_tool(
        [PYTHON_EXE if os.path.exists(os.path.abspath("tools/browser.py")) else "node",
         os.path.abspath("tools/browser.py") if os.path.exists(os.path.abspath("tools/browser.py")) else os.path.abspath("tools/browser.js"),
         "--open", url, "--click", selector, "--duration", str(duration)]
    )

def _browser_screenshot():
    """Быстрый скриншот браузера для отладки"""
    os.makedirs("logs", exist_ok=True)
    screenshot_path = os.path.abspath("logs/last.png")
    cmd = [PYTHON_EXE if os.path.exists(os.path.abspath("tools/browser.py")) else "node",
           os.path.abspath("tools/browser.py") if os.path.exists(os.path.abspath("tools/browser.py")) else os.path.abspath("tools/browser.js"),
           "--screenshot", screenshot_path]
    result = run_tool(cmd)
    if result.get("ok"):
        result["screenshot_path"] = screenshot_path
    return result

# ═══════════════════════════════════════════════════════════════
# 🌐 HTTP КЛИЕНТ ДЛЯ БРАУЗЕР-СЕРВИСА 🌐
# ═══════════════════════════════════════════════════════════════

def _post(path, json_data, timeout=30):
    """HTTP POST запрос к браузер-сервису"""
    try:
        r = requests.post(f"{BROWSERD_URL}{path}", json=json_data, timeout=timeout)
        return {"ok": r.ok, "rc": 0 if r.ok else 1, "out": r.text, "err": "", "cmd": [path, json_data]}
    except Exception as e:
        return {"ok": False, "rc": 1, "out": "", "err": str(e), "cmd": [path, json_data]}

def _get(path, timeout=10):
    """HTTP GET запрос к браузер-сервису"""
    try:
        r = requests.get(f"{BROWSERD_URL}{path}", timeout=timeout)
        return {"ok": r.ok, "rc": 0 if r.ok else 1, "out": r.text, "err": "", "cmd": [path]}
    except Exception as e:
        return {"ok": False, "rc": 1, "out": "", "err": str(e), "cmd": [path]}

# Обертки с allowlist-проверками для новых браузерных инструментов
def _browser_service_open(url, duration=10, auto_play=False):
    """Открытие URL через браузер-сервис с проверкой allowlist"""
    allowed, host = is_allowed_url(url)
    if not allowed:
        return {"ok": False, "error": "host_not_allowed", "host": host, 
                "hint": "Домен не разрешен. Добавьте его в config/allowed_hosts.txt или получите подтверждение пользователя."}
    return _post("/open", {"url": url, "duration": duration, "auto_play": bool(auto_play)})

def _browser_service_play_audio(page_url, audio_url, duration=5):
    """Воспроизведение аудио через браузер-сервис с проверкой allowlist"""
    if page_url:
        allowed_page, host_page = is_allowed_url(page_url)
        if not allowed_page:
            return {"ok": False, "error": "host_not_allowed", "host": host_page,
                    "hint": "Домен страницы не разрешен. Добавьте его в config/allowed_hosts.txt"}
    
    allowed_audio, host_audio = is_allowed_url(audio_url)
    if not allowed_audio:
        return {"ok": False, "error": "host_not_allowed", "host": host_audio,
                "hint": "Домен аудио не разрешен. Добавьте его в config/allowed_hosts.txt"}
    
    return _post("/play_audio", {"page_url": page_url, "audio_url": audio_url, "duration": duration})

TOOLS = {
    "audio.play": lambda source, volume=80: run_tool(
        [PYTHON_EXE, os.path.abspath("tools/audio.py"), "--source", source, "--volume", str(volume)]
    ),
    "audio.pause": lambda: run_tool(
        [PYTHON_EXE, os.path.abspath("tools/audio.py"), "--pause"]
    ),
    "audio.resume": lambda: run_tool(
        [PYTHON_EXE, os.path.abspath("tools/audio.py"), "--resume"]
    ),
    "audio.setVolume": lambda volume: run_tool(
        [PYTHON_EXE, os.path.abspath("tools/audio.py"), "--set-volume", str(volume)]
    ),
    "audio.stop": lambda: run_tool(["cmd", "/c", os.path.abspath("scripts/stopaudio.cmd")]),
    
    # Старые браузерные инструменты (прямые через Playwright)
    "browser.open": lambda url, duration=10, auto_play=False: _browser_open_safe(url, duration, auto_play),
    "browser.playAudio": lambda page_url, audio_url, duration=10: _browser_play_audio_safe(page_url, audio_url, duration),
    "browser.click": lambda url, selector, duration=5: _browser_click_safe(url, selector, duration),
    "browser.screenshot": lambda: _browser_screenshot(),
    
    # Новые инструменты браузер-сервиса (через HTTP API)
    "browser.service.start": lambda port=8787: run_tool(["cmd", "/c", os.path.abspath("scripts/browserd-start.cmd"), str(port)], timeout=0),
    "browser.service.stop": lambda: run_tool(["cmd", "/c", os.path.abspath("scripts/browserd-stop.cmd")]),
    "browser.service.health": lambda: _get("/health"),
    "browser.service.open": lambda url, duration=10, auto_play=False: _browser_service_open(url, duration, auto_play),
    "browser.service.playAudio": lambda page_url, audio_url, duration=5: _browser_service_play_audio(page_url, audio_url, duration),
    "browser.service.click": lambda selector, timeout_ms=3000: _post("/click", {"selector": selector, "timeout_ms": timeout_ms}),
    "browser.service.screenshot": lambda path="logs/last.png": _post("/screenshot", {"path": path}),
    
    # Новые аудио-команды плейлиста (MediaListPlayer)
    "audio.queue": lambda items: run_tool([PYTHON_EXE, os.path.abspath("tools/audio.py"), "queue", "--add", *items]),
    "audio.next": lambda volume=80: run_tool([PYTHON_EXE, os.path.abspath("tools/audio.py"), "next", "--volume", str(volume)]),
    "audio.status": lambda: run_tool([PYTHON_EXE, os.path.abspath("tools/audio.py"), "status"])
}

def handle_tool_call(payload: dict):
    name = payload.get("tool")
    args = payload.get("args", {}) or {}
    
    # Логируем вызов инструмента
    logger.info("TOOL %s ARGS %s", name, args)
    
    if name not in TOOLS:
        result = {"ok": False, "error": f"Unknown tool: {name}"}
        logger.warning("TOOL %s UNKNOWN", name)
        return result
    
    try:
        result = TOOLS[name](**args)
        # Логируем результат (сокращенно, чтобы не засорять логи)
        result_summary = {
            "ok": result.get("ok"),
            "rc": result.get("rc"),
            "error": result.get("error"),
            "timeout": result.get("timeout")
        }
        logger.info("TOOL %s RESULT %s", name, result_summary)
        return result  # Возвращаем результат run_tool с ok/rc/out/err/cmd
    except TypeError as e:
        result = {"ok": False, "error": f"Bad args: {e}"}
        logger.error("TOOL %s BAD_ARGS %s", name, e)
        return result
    except Exception as e:
        result = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        logger.error("TOOL %s EXCEPTION %s", name, e)
        return result
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
if os.getenv('OPEN_INTERPRETER_COMPUTER_IMPORT', 'true').lower() == 'true':
    interpreter.computer_import = True

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

🎵 МУЗЫКА И АУДИО (ПРИОРИТЕТ: VLC):

🔊 ОСНОВНОЙ АУДИО ДВИЖОК - VLC MediaListPlayer:
```python
# ВСЕГДА используй эти функции для воспроизведения аудио
import json, subprocess, os

def play_audio(source, volume=80):
    """Воспроизведение аудио через VLC - ПЕРВЫЙ ВЫБОР для любой музыки"""
    result = subprocess.run([
        r"c:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        os.path.abspath("tools/audio.py"), 
        "--source", source, 
        "--volume", str(volume)
    ], capture_output=True, text=True, timeout=10)
    return result.stdout.strip()

def pause_audio():
    """Пауза VLC"""
    result = subprocess.run([
        r"c:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        os.path.abspath("tools/audio.py"), "--pause"
    ], capture_output=True, text=True, timeout=5)
    return result.stdout.strip()

def resume_audio():
    """Возобновление VLC"""
    result = subprocess.run([
        r"c:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        os.path.abspath("tools/audio.py"), "--resume"
    ], capture_output=True, text=True, timeout=5)
    return result.stdout.strip()

def stop_audio():
    """Остановка VLC"""
    result = subprocess.run([
        r"c:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        os.path.abspath("tools/audio.py"), "--stop"
    ], capture_output=True, text=True, timeout=5)
    return result.stdout.strip()

def queue_audio(*urls):
    """Добавление в плейлист VLC"""
    result = subprocess.run([
        r"c:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        os.path.abspath("tools/audio.py"), "queue", "--add"
    ] + list(urls), capture_output=True, text=True, timeout=5)
    return result.stdout.strip()

def next_audio(volume=80):
    """Следующий трек в VLC плейлисте"""
    result = subprocess.run([
        r"c:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        os.path.abspath("tools/audio.py"), "next", "--volume", str(volume)
    ], capture_output=True, text=True, timeout=5)
    return result.stdout.strip()

def audio_status():
    """Статус VLC плеера"""
    result = subprocess.run([
        r"c:\Users\user\Desktop\Open Interpreter\.venv\Scripts\python.exe",
        os.path.abspath("tools/audio.py"), "status"
    ], capture_output=True, text=True, timeout=5)
    return result.stdout.strip()
```

🎭 ЗАПАСНЫЕ БРАУЗЕРНЫЕ ФУНКЦИИ (используй только если VLC не работает):
- play_yandex_music() - поиск и воспроизведение в Яндекс.Музыке
- play_audio_in_browser(audio_url, duration=30) - воспроизведение аудио в браузере
- smart_media_control() - управление различными медиа приложениями
- smart_media_control() - управление различными медиа приложениями

🌐 БРАУЗЕР И ВЕБ:
- open_browser_url(url, duration=10) - открытие URL в браузере через Playwright
- browser_click_element(selector, url=None, duration=5) - клик по элементу в браузере
- Поддержка автовоспроизведения аудио в браузере
- Управление Яндекс.Музыкой через браузер

🖱️ УПРАВЛЕНИЕ ИНТЕРФЕЙСОМ:
- computer.take_screenshot() - делает скриншот экрана
- computer.click_image('path/to/image.png') - находит и кликает по изображению
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
# ПЕРВЫЙ ВЫБОР - VLC прямое воспроизведение
result = play_audio('https://samplelib.com/lib/preview/mp3/sample-3s.mp3', volume=70)
print(f"VLC воспроизведение: {result}")

# Если нужен поиск - пробуем smart media control только для поиска
if "нет URL" in result:
    result2 = smart_media_control('play')
    print(f"Поиск музыки: {result2}")
```

Пользователь: "Поставь на паузу"
Ответ:
```python
# ВСЕГДА сначала пробуем VLC
result = pause_audio()
print(f"VLC пауза: {result}")
```

Пользователь: "Следующий трек"
Ответ:
```python
# VLC плейлист
result = next_audio(volume=80)
print(f"VLC следующий: {result}")
```

Пользователь: "Включи эту песню: URL"
Ответ:
```python
# Всегда VLC для прямых URL
result = play_audio("URL", volume=80)
print(f"Воспроизведение: {result}")
```

Пользователь: "Добавь в плейлист: URL1, URL2"
Ответ:
```python
# VLC очередь
result = queue_audio("URL1", "URL2")
print(f"Плейлист: {result}")
```

Пользователь: "Статус плеера"
Ответ:
```python
# Проверяем VLC статус
result = audio_status()
print(f"VLC статус: {result}")
```

🎭 БРАУЗЕРНЫЕ МЕТОДЫ (только если VLC недоступен):

Пользователь: "Найди и включи песню Баста - Сансара" (если VLC не может найти)
Ответ:
```python
# Запасной вариант - Яндекс.Музыка для поиска
result = play_yandex_music('Баста Сансара')
print(f"Поиск в Яндекс: {result}")
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

- Персистентный браузер:
  - старт: {"type":"tool_call","tool":"browser.service.start","args":{"port":8787}}
  - здоровье: {"type":"tool_call","tool":"browser.service.health","args":{}}
  - открыть: {"type":"tool_call","tool":"browser.open","args":{"url":"<URL>","auto_play":false,"duration":5}}
  - проиграть аудио: {"type":"tool_call","tool":"browser.playAudio","args":{"page_url":"<URL>","audio_url":"<URL>","duration":5}}
  - клик: {"type":"tool_call","tool":"browser.click","args":{"selector":"<CSS>"}}
  - скриншот: {"type":"tool_call","tool":"browser.screenshot","args":{"path":"logs/last.png"}}
  - стоп: {"type":"tool_call","tool":"browser.service.stop","args":{}}

- Плейлисты аудио:
  - очередь: {"type":"tool_call","tool":"audio.queue","args":{"items":["<URL1>","<URL2>"]}}
  - следующий: {"type":"tool_call","tool":"audio.next","args":{"volume":80}}
  - статус: {"type":"tool_call","tool":"audio.status","args":{}}

- Для управления браузером (старый API): 
  - открыть URL: {"type":"tool_call","tool":"browser.open","args":{"url":"<URL>","duration":10}}
  - открыть страницу и воспроизвести аудио: {"tool":"browser.playAudio","args":{"page_url":"<URL>","audio_url":"<URL>","duration":10}}
  - клик по элементу: {"type":"tool_call","tool":"browser.click","args":{"url":"<URL>","selector":"<CSS_селектор>","duration":5}}
  - скриншот для отладки: {"type":"tool_call","tool":"browser.screenshot","args":{}}

🔒 БЕЗОПАСНОСТЬ URL:
- Перед открытием URL с неразрешенным доменом ВСЕГДА спрашивай подтверждение пользователя
- Если домен не в allowlist - предупреди пользователя и попроси разрешение
- Объясни риски посещения неизвестных сайтов

Не выполняй произвольные shell-команды. Используй только эти инструменты.
"""

interpreter.system_message = computer_skills_prompt

# Импортируем и регистрируем компьютерные утилиты
try:
    from computer_utils import (
        find_and_launch_music_app, control_media, find_application, 
        search_files, take_screenshot, click_image, type_text, press_keys, computer,
        smart_media_control, find_and_control_spotify, launch_music_app,
        advanced_click_by_image, smart_window_control
    )
    logger.info("✅ Компьютерные утилиты загружены")
    
    # Импортируем системы памяти и Яндекс.Музыки
    try:
        from memory_system import memory_system
        logger.info("✅ Система памяти загружена")
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
    __main__.click_image = click_image
    __main__.type_text = type_text
    __main__.press_keys = press_keys
    __main__.computer = computer
    
    # Новые улучшенные функции
    __main__.smart_media_control = smart_media_control
    __main__.find_and_control_spotify = find_and_control_spotify
    __main__.launch_music_app = launch_music_app
    __main__.advanced_click_by_image = advanced_click_by_image
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

# VLC audio priority system message уже установлен в строке 714
# Не перезаписываем его здесь



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
                            
                            # Очищаем историю перед выполнением для избежания конфликтов
                            interpreter.messages = []
                            
                            # ВАЖНО: Отключаем проблемные функции HTML/jupyter перед выполнением
                            for attempts in range(3):  # 3 попытки
                                try:
                                    response = interpreter.chat(user_message)
                                    break  # Если успешно, выходим из цикла
                                except Exception as retry_error:
                                    if "path should be string" in str(retry_error) and attempts < 2:
                                        logger.warning(f"Попытка {attempts + 1}: {retry_error}")
                                        # Очищаем состояние перед повтором
                                        interpreter.messages = []
                                        continue
                                    else:
                                        raise retry_error  # Если все попытки исчерпаны
                            
                            # Формируем ответ
                            full_response = ""
                            if isinstance(response, list):
                                for chunk in response:
                                    if isinstance(chunk, dict):
                                        if chunk.get("type") == "message" and chunk.get("role") == "assistant":
                                            if "content" in chunk:
                                                content = chunk["content"]
                                                if isinstance(content, str):
                                                    full_response += content
                                                elif isinstance(content, list):
                                                    for item in content:
                                                        if isinstance(item, dict) and item.get("type") == "text":
                                                            full_response += item.get("text", "")
                                        elif chunk.get("type") == "code":
                                            await self.send_to_client(websocket, {
                                                "type": "code",
                                                "content": chunk.get("content", ""),
                                                "language": chunk.get("format", "python")
                                            })
                                        elif chunk.get("type") == "confirmation":
                                            await self.send_to_client(websocket, {
                                                "type": "confirmation",
                                                "message": chunk.get("content", "")
                                            })
                            
                            # Отправляем финальный ответ
                            if full_response.strip():
                                await self.send_to_client(websocket, {
                                    "type": "message",
                                    "content": full_response.strip()
                                })
                            
                            # Отправляем статус завершения
                            await self.send_to_client(websocket, {
                                "type": "completion",
                                "message": "✅ Задача выполнена"
                            })
                            
                        except Exception as e:
                            error_msg = str(e)
                            logger.error(f"Ошибка выполнения: {error_msg}")
                            await self.send_to_client(websocket, {
                                "type": "error",
                                "message": f"❌ Ошибка: {error_msg}"
                            })
                
                except json.JSONDecodeError:
                    await self.send_to_client(websocket, {
                        "type": "error",
                        "message": "❌ Неверный формат JSON"
                    })
                except Exception as e:
                    logger.error(f"Ошибка обработки сообщения: {e}")
                    await self.send_to_client(websocket, {
                        "type": "error",
                        "message": f"❌ Ошибка обработки: {str(e)}"
                    })
        
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

server_instance = OpenInterpreterServer()

async def run_server():
    port = int(os.getenv('OI_WS_PORT', 8765))
    logger.info(f"🚀 Запуск WebSocket сервера на порту {port}")
    logger.info(f"🔗 WebSocket URL: ws://localhost:{port}")
    
    try:
        async with websockets.serve(server_instance.handle_message, "localhost", port):
            logger.info("✅ WebSocket сервер запущен успешно")
            await asyncio.Future()  # Работаем бесконечно
    except Exception as e:
        logger.error(f"❌ Ошибка запуска сервера: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(run_server())
