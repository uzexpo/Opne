#!/usr/bin/env python3
"""
Упрощенный smoke тест инструментов без WebSocket
"""
import sys
import os
sys.path.append(os.path.abspath('.'))

from server import TOOLS

def test_tool(name, args, description):
    print(f"\n=== {description} ===")
    try:
        result = TOOLS[name](**args)
        print(f"✓ {name}: SUCCESS")
        print(f"  Result: {result.get('ok', False)}")
        if result.get('out'):
            print(f"  Output: {result['out'][:100]}...")
        return True
    except Exception as e:
        print(f"✗ {name}: FAILED - {e}")
        return False

def main():
    print("=== SMOKE TEST - DIRECT TOOL CALLS ===")
    
    results = []
    
    # Test 1: Audio status
    results.append(test_tool("audio.status", {}, "Проверка статуса аудио очереди"))
    
    # Test 2: Audio queue
    results.append(test_tool("audio.queue", 
                            {"items": ["https://samplelib.com/lib/preview/mp3/sample-3s.mp3"]}, 
                            "Добавление в аудио очередь"))
    
    # Test 3: Browser service start
    results.append(test_tool("browser.service.start", {"port": 8787}, "Запуск браузер-сервиса"))
    
    # Test 4: Browser service health (может не работать если сервис не успел запуститься)
    results.append(test_tool("browser.service.health", {}, "Проверка здоровья браузер-сервиса"))
    
    # Test 5: Browser service stop
    results.append(test_tool("browser.service.stop", {}, "Остановка браузер-сервиса"))
    
    # Test 6: Browser screenshot (старый API)
    results.append(test_tool("browser.screenshot", {}, "Скриншот браузера"))
    
    print(f"\n=== РЕЗУЛЬТАТЫ ===")
    passed = sum(results)
    total = len(results)
    print(f"Пройдено: {passed}/{total}")
    
    # Проверяем создался ли скриншот
    screenshot_path = "logs/last.png"
    if os.path.exists(screenshot_path):
        print(f"✓ Скриншот создан: {screenshot_path}")
    else:
        print(f"✗ Скриншот не найден: {screenshot_path}")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
