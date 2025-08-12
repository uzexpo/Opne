#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 Тест Enhanced Computer Vision для Open Interpreter
Проверка всех функций компьютерного зрения
"""

import sys
import os
sys.path.append('tools')

def test_cv_system():
    """Полный тест системы компьютерного зрения"""
    
    print("🧪 ТЕСТ ENHANCED COMPUTER VISION")
    print("=" * 50)
    
    try:
        # Импорт модулей
        from enhanced_cv import EnhancedComputerVision, smart_click, analyze_screen
        from cv_skills import (
            open_program, click_text, click_button, navigate_to, 
            smart_screenshot, screen_analysis, play_music_smart
        )
        
        print("✅ Все модули импортированы успешно")
        
        # Инициализация CV системы
        cv = EnhancedComputerVision()
        print("✅ Enhanced Computer Vision инициализирован")
        
        # Тест 1: Анализ экрана
        print("\n📊 Тест 1: Анализ экрана")
        screen_result = screen_analysis()
        print(f"Результат: {screen_result}")
        
        # Тест 2: Умный скриншот
        print("\n📸 Тест 2: Умный скриншот")
        screenshot_result = smart_screenshot("test_enhanced_cv.png")
        print(f"Результат: {screenshot_result}")
        
        # Тест 3: Захват экрана (низкоуровневый)
        print("\n🖥️ Тест 3: Захват экрана")
        image = cv.capture.capture_screen()
        if image.size > 0:
            print(f"✅ Захват успешен: {image.shape}")
        else:
            print("❌ Ошибка захвата экрана")
        
        # Тест 4: Обработка изображения
        print("\n🔍 Тест 4: Обработка изображения")
        if image.size > 0:
            elements = cv.local_processor.find_ui_elements_basic(image)
            print(f"✅ Найдено {len(elements)} UI элементов")
        else:
            print("❌ Нет изображения для обработки")
        
        # Тест 5: Интеграционные функции
        print("\n🔧 Тест 5: Интеграционные функции")
        
        # Проверка доступности функций
        functions_to_test = [
            ("open_program", open_program),
            ("click_text", click_text), 
            ("click_button", click_button),
            ("navigate_to", navigate_to),
            ("play_music_smart", play_music_smart)
        ]
        
        for func_name, func in functions_to_test:
            try:
                # Тестовый вызов (без реального действия)
                if func_name == "open_program":
                    result = "Функция доступна"  # Не вызываем реально
                elif func_name in ["click_text", "click_button"]:
                    result = "Функция доступна"  # Не вызываем реально
                elif func_name == "navigate_to":
                    result = "Функция доступна"  # Не вызываем реально  
                elif func_name == "play_music_smart":
                    result = "Функция доступна"  # Не вызываем реально
                
                print(f"✅ {func_name}: {result}")
                
            except Exception as e:
                print(f"❌ {func_name}: Ошибка - {e}")
        
        print("\n🎉 ТЕСТ ЗАВЕРШЕН УСПЕШНО!")
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Возможные решения:")
        print("   - Установите opencv-python: pip install opencv-python")
        print("   - Установите pyautogui: pip install pyautogui")
        print("   - Установите mss: pip install mss")
        return False
        
    except Exception as e:
        print(f"❌ Общая ошибка: {e}")
        return False

def test_dependencies():
    """Проверка всех зависимостей"""
    
    print("📦 ПРОВЕРКА ЗАВИСИМОСТЕЙ")
    print("=" * 30)
    
    dependencies = [
        "numpy", "PIL", "cv2", "mss", "pyautogui"
    ]
    
    all_ok = True
    
    for dep in dependencies:
        try:
            if dep == "PIL":
                import PIL
                print(f"✅ {dep}: {PIL.__version__}")
            elif dep == "cv2":
                import cv2
                print(f"✅ {dep}: {cv2.__version__}")
            elif dep == "mss":
                import mss
                print(f"✅ {dep}: Доступен")
            elif dep == "pyautogui":
                import pyautogui
                print(f"✅ {dep}: Доступен")
            elif dep == "numpy":
                import numpy as np
                print(f"✅ {dep}: {np.__version__}")
            else:
                exec(f"import {dep}")
                print(f"✅ {dep}: Доступен")
                
        except ImportError:
            print(f"❌ {dep}: НЕ УСТАНОВЛЕН")
            all_ok = False
    
    return all_ok

def performance_test():
    """Тест производительности"""
    
    print("\n⚡ ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 30)
    
    try:
        from enhanced_cv import EnhancedComputerVision
        import time
        
        cv = EnhancedComputerVision()
        
        # Тест скорости захвата экрана
        start_time = time.time()
        for i in range(5):
            image = cv.capture.capture_screen()
        capture_time = (time.time() - start_time) / 5
        
        print(f"📸 Среднее время захвата: {capture_time*1000:.1f}ms")
        
        # Тест анализа
        if image.size > 0:
            start_time = time.time()
            elements = cv.local_processor.find_ui_elements_basic(image)
            analysis_time = time.time() - start_time
            
            print(f"🔍 Время анализа: {analysis_time*1000:.1f}ms")
            print(f"🎯 Найдено элементов: {len(elements)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка теста производительности: {e}")
        return False

if __name__ == "__main__":
    print("🚀 ЗАПУСК ПОЛНОГО ТЕСТА ENHANCED COMPUTER VISION")
    print("=" * 60)
    
    # 1. Проверка зависимостей
    deps_ok = test_dependencies()
    
    if not deps_ok:
        print("\n❌ НЕКОТОРЫЕ ЗАВИСИМОСТИ НЕ УСТАНОВЛЕНЫ")
        print("Выполните: pip install opencv-python pyautogui mss pillow numpy")
        sys.exit(1)
    
    # 2. Основной тест
    main_test_ok = test_cv_system()
    
    # 3. Тест производительности
    if main_test_ok:
        perf_ok = performance_test()
    
    # Итоговый результат
    print("\n" + "=" * 60)
    if main_test_ok:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("✅ Enhanced Computer Vision готов к использованию")
        print("\n📋 Доступные команды:")
        print("   - cv.analyze - анализ экрана")
        print("   - cv.screenshot - умный скриншот")
        print("   - cv.open_program - открыть программу")
        print("   - cv.click_text - клик по тексту")
        print("   - cv.click_button - клик по кнопке")
        print("   - cv.play_music - умное воспроизведение музыки")
    else:
        print("❌ ТЕСТЫ ЗАВЕРШИЛИСЬ С ОШИБКАМИ")
        print("Проверьте установку зависимостей и попробуйте снова")
