#!/usr/bin/env python3
"""Тест логирования в файл через tool_call"""

import os
import sys
from urllib.parse import urlparse

# Импортируем logger из server
import logging
from logging.handlers import RotatingFileHandler

os.makedirs("logs", exist_ok=True)
logger = logging.getLogger("agent")
logger.setLevel(logging.INFO)
fh = RotatingFileHandler("logs/agent.log", maxBytes=2_000_000, backupCount=3, encoding="utf-8")
fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
fh.setFormatter(fmt)
logger.addHandler(fh)

def run_tool(cmd: list[str], timeout: int = 120):
    """Универсальный запуск инструментов с расширенным логированием"""
    import subprocess
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "ok": proc.returncode == 0,
            "rc": proc.returncode,
            "out": proc.stdout[-2000:] if proc.stdout else "",
            "err": proc.stderr[-2000:] if proc.stderr else "",
            "cmd": cmd
        }
    except subprocess.TimeoutExpired as e:
        return {"ok": False, "timeout": True, "out": e.stdout[-2000:] if e.stdout else "", "err": e.stderr[-2000:] if e.stderr else "", "cmd": cmd}
    except Exception as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}", "cmd": cmd}

def handle_tool_call(payload: dict):
    name = payload.get("tool")
    args = payload.get("args", {}) or {}
    
    # Логируем вызов инструмента
    logger.info("TOOL %s ARGS %s", name, args)
    
    # Простые инструменты для теста
    TOOLS = {
        "audio.stop": lambda: run_tool(["cmd", "/c", "echo", "VLC stopped"]),
        "test.echo": lambda message="test": run_tool(["cmd", "/c", "echo", message])
    }
    
    if name not in TOOLS:
        result = {"ok": False, "error": f"Unknown tool: {name}"}
        logger.warning("TOOL %s UNKNOWN", name)
        return result
    
    try:
        result = TOOLS[name](**args)
        # Логируем результат (сокращенно)
        result_summary = {
            "ok": result.get("ok"),
            "rc": result.get("rc"),
            "error": result.get("error"),
            "timeout": result.get("timeout")
        }
        logger.info("TOOL %s RESULT %s", name, result_summary)
        return result
    except TypeError as e:
        result = {"ok": False, "error": f"Bad args: {e}"}
        logger.error("TOOL %s BAD_ARGS %s", name, e)
        return result
    except Exception as e:
        result = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        logger.error("TOOL %s EXCEPTION %s", name, e)
        return result

if __name__ == "__main__":
    print("🧪 Тестирование логирования tool_call...")
    
    # Логируем информацию о старте
    logger.info("Testing session started")
    logger.info("Python interpreter: %s", sys.executable)
    logger.info("Working directory: %s", os.getcwd())
    
    # Тест 1: успешный вызов
    result1 = handle_tool_call({"tool": "test.echo", "args": {"message": "Hello World"}})
    print(f"Тест 1: {result1}")
    
    # Тест 2: неизвестный инструмент
    result2 = handle_tool_call({"tool": "unknown.tool", "args": {}})
    print(f"Тест 2: {result2}")
    
    # Тест 3: неправильные аргументы
    result3 = handle_tool_call({"tool": "test.echo", "args": {"wrong_param": "value"}})
    print(f"Тест 3: {result3}")
    
    logger.info("Testing session completed")
    print("✅ Логи сохранены в logs/agent.log")
