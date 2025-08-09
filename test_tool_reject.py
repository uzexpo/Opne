#!/usr/bin/env python3
"""Тест отклонения tool_call из-за недопустимого домена"""

import os
import sys
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
    return {"ok": True, "message": f"Would open {url} for {duration}s", "host": host}

def _browser_play_audio_safe(page_url, audio_url, duration=10):
    allowed_page, host_page = is_allowed_url(page_url)
    allowed_audio, host_audio = is_allowed_url(audio_url)
    if not allowed_page:
        return {"ok": False, "error": "host_not_allowed", "host": host_page, "hint": "add host to config/allowed_hosts.txt"}
    if not allowed_audio:
        return {"ok": False, "error": "host_not_allowed", "host": host_audio, "hint": "add host to config/allowed_hosts.txt"}
    return {"ok": True, "message": f"Would play {audio_url} on {page_url} for {duration}s"}

if __name__ == "__main__":
    print("🧪 Тестирование отклонения недопустимых tool_call...")
    
    # Тест 1: разрешенный домен
    result1 = _browser_open_safe("https://youtube.com/watch?v=test", 5)
    print(f"\n📋 Тест 1 - youtube.com (разрешен):")
    print(f"  {result1}")
    
    # Тест 2: запрещенный домен
    result2 = _browser_open_safe("https://malicious-hacker-site.evil", 5)
    print(f"\n📋 Тест 2 - malicious-hacker-site.evil (запрещен):")
    print(f"  {result2}")
    
    # Тест 3: browser.playAudio с запрещенным аудио URL
    result3 = _browser_play_audio_safe("https://youtube.com/watch?v=test", "https://evil-site.com/virus.mp3", 5)
    print(f"\n📋 Тест 3 - youtube.com + evil-site.com (смешанный):")
    print(f"  {result3}")
    
    print("\n✅ Все тесты tool_call отклонения завершены!")
