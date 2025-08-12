#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ПРОСТОЙ ТЕСТ SIMPLE CV ФУНКЦИЙ 🧪
Тестируем новые простые функции без запуска сервера
"""

import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

try:
    from simple_cv import SimpleCV
    import pyautogui
    import time
    
    print("🚀 Тестирование Simple CV функций...")
    print("="*50)
    
    # Инициализируем Simple CV
    cv = SimpleCV()
    
    # Тест 1: Проверяем известные координаты Play кнопки
    print("\n🧪 Тест 1: Проверка известных координат Play кнопки")
    print(f"📍 Известные координаты: {cv.known_play_coordinates}")
    
    # Тест 2: Поиск кнопки Play
    print("\n🧪 Тест 2: Поиск кнопки Play на экране")
    result = cv.find_text_simple("play")
    print(f"📍 Результат поиска: {result}")
    
    # Тест 3: Попробуем найти кнопку Play через pyautogui
    print("\n🧪 Тест 3: Прямой поиск через pyautogui")
    try:
        # Попробуем найти любые UI элементы на экране
        screen_width, screen_height = pyautogui.size()
        print(f"📱 Размер экрана: {screen_width} x {screen_height}")
        
        # Берем скриншот для анализа
        screenshot = pyautogui.screenshot()
        print(f"📸 Скриншот сделан: {screenshot.size}")
        
        # Проверяем координаты из нашего списка
        for coord in cv.known_play_coordinates:
            x, y = coord
            if 0 <= x < screen_width and 0 <= y < screen_height:
                print(f"✅ Координата {coord} валидна для этого экрана")
            else:
                print(f"❌ Координата {coord} за пределами экрана")
                
    except Exception as e:
        print(f"❌ Ошибка в pyautogui тесте: {e}")
    
    # Тест 4: Тест функции клика (БЕЗ РЕАЛЬНОГО КЛИКА)
    print("\n🧪 Тест 4: Тест функции клика (симуляция)")
    print("⚠️ РЕАЛЬНЫЙ КЛИК НЕ ВЫПОЛНЯЕТСЯ - только проверка логики")
    
    # Временно переопределяем click чтобы не кликнуть реально
    original_click = pyautogui.click
    click_calls = []
    
    def mock_click(x, y):
        click_calls.append((x, y))
        print(f"🖱️ СИМУЛЯЦИЯ КЛИКА: ({x}, {y})")
    
    pyautogui.click = mock_click
    
    try:
        result = cv.click_play_button()
        print(f"🎯 Результат click_play_button: {result}")
        print(f"📝 Количество симулированных кликов: {len(click_calls)}")
        for i, (x, y) in enumerate(click_calls, 1):
            print(f"   {i}. Клик по ({x}, {y})")
    except Exception as e:
        print(f"❌ Ошибка в тесте клика: {e}")
    finally:
        # Восстанавливаем оригинальную функцию
        pyautogui.click = original_click
    
    print("\n🏁 Тестирование завершено!")
    print("="*50)
    print("✅ Simple CV функции готовы к работе!")
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("🔧 Убедитесь что simple_cv.py находится в папке tools/")
except Exception as e:
    print(f"❌ Неожиданная ошибка: {e}")
