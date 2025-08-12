#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🧪 ТЕСТ ENHANCED COMPUTER VISION 🧪
Проверяем, работает ли наша система CV
"""

import sys
import os

# Добавляем пути
current_dir = os.path.dirname(os.path.abspath(__file__))
tools_path = os.path.join(current_dir, "tools")
sys.path.append(tools_path)
sys.path.append(current_dir)

print("🔍 Тестирование Enhanced Computer Vision...")
print(f"📁 Текущая директория: {current_dir}")
print(f"🔧 Путь к tools: {tools_path}")

# Проверяем импорты
try:
    print("\n1️⃣ Тестируем импорт enhanced_cv...")
    from tools.enhanced_cv import EnhancedComputerVision
    print("✅ enhanced_cv импортирован успешно!")
    
    cv = EnhancedComputerVision()
    print("✅ EnhancedComputerVision создан успешно!")
    
except Exception as e:
    print(f"❌ Ошибка импорта enhanced_cv: {e}")

try:
    print("\n2️⃣ Тестируем импорт cv_skills...")
    from tools.cv_skills import CVNavigationSkills, open_program, click_text, click_button
    print("✅ cv_skills импортированы успешно!")
    
    cv_skills = CVNavigationSkills()
    print("✅ CVNavigationSkills создан успешно!")
    
except Exception as e:
    print(f"❌ Ошибка импорта cv_skills: {e}")

try:
    print("\n3️⃣ Тестируем импорт yandex_music_cv...")
    from tools.yandex_music_cv import YandexMusicCV, play_yandex_music_with_cv
    print("✅ yandex_music_cv импортирован успешно!")
    
    yandex_cv = YandexMusicCV()
    print("✅ YandexMusicCV создан успешно!")
    
except Exception as e:
    print(f"❌ Ошибка импорта yandex_music_cv: {e}")

# Тестируем функциональность
try:
    print("\n4️⃣ Тестируем скриншот...")
    import pyautogui
    screenshot = pyautogui.screenshot()
    print(f"✅ Скриншот сделан! Размер: {screenshot.size}")
    
except Exception as e:
    print(f"❌ Ошибка скриншота: {e}")

try:
    print("\n5️⃣ Тестируем Enhanced CV анализ...")
    
    # Простой тест CV
    if 'cv' in locals():
        result = cv.smart_screenshot()
        print(f"✅ Smart screenshot: {type(result)}")
        
        # Тест click_text
        if 'click_text' in locals():
            test_result = click_text("test", dry_run=True)
            print(f"✅ click_text тест: {test_result}")
    
except Exception as e:
    print(f"❌ Ошибка тестирования CV: {e}")

# Тестируем pyautogui напрямую
try:
    print("\n6️⃣ Тестируем pyautogui...")
    import pyautogui
    
    # Получаем позицию мыши
    x, y = pyautogui.position()
    print(f"✅ Позиция мыши: ({x}, {y})")
    
    # Получаем размер экрана
    width, height = pyautogui.size()
    print(f"✅ Размер экрана: {width}x{height}")
    
    print("✅ pyautogui работает корректно!")
    
except Exception as e:
    print(f"❌ Ошибка pyautogui: {e}")

print("\n🏁 Тест завершен!")
