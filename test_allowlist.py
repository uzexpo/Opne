#!/usr/bin/env python3
"""Тест allowlist доменов"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем функции из server.py
from urllib.parse import urlparse

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

def _browser_open_safe(url, duration=10):
    allowed, host = is_allowed_url(url)
    if not allowed:
        return {"ok": False, "error": "host_not_allowed", "host": host, "hint": "add host to config/allowed_hosts.txt"}
    return {"ok": True, "message": f"Would open {url} for {duration}s"}

if __name__ == "__main__":
    print("🧪 Тестирование allowlist доменов...")
    
    # Тест 1: разрешенный домен
    result1 = _browser_open_safe("https://youtube.com/watch?v=test")
    print(f"\n📋 Тест 1 - youtube.com (разрешен):")
    print(f"  {result1}")
    
    # Тест 2: поддомен разрешенного домена
    result2 = _browser_open_safe("https://www.youtube.com/watch?v=test")
    print(f"\n📋 Тест 2 - www.youtube.com (поддомен):")
    print(f"  {result2}")
    
    # Тест 3: запрещенный домен
    result3 = _browser_open_safe("https://malicious-site.com/hack")
    print(f"\n📋 Тест 3 - malicious-site.com (запрещен):")
    print(f"  {result3}")
    
    # Тест 4: проверяем содержимое allowlist файла
    print(f"\n📋 Содержимое config/allowed_hosts.txt:")
    with open("config/allowed_hosts.txt", "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            print(f"  {line_num}: {line.strip()}")
    
    print("\n✅ Все тесты allowlist завершены!")
