#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎵 ПРОСТОЙ ТЕСТ КНОПКИ PLAY 🎵
Тестируем поиск и клик по кнопке Play в Яндекс.Музыке
"""

import pyautogui
import time
import sys
import os

print("🎵 Тестирование поиска кнопки Play...")

def simple_play_test():
    """Простой тест поиска кнопки Play"""
    try:
        print("📸 Делаем скриншот...")
        screenshot = pyautogui.screenshot()
        print(f"✅ Скриншот получен: {screenshot.size}")
        
        print("🔍 Ищем текст 'Play' на экране...")
        try:
            # Поиск текста "Play" на экране
            play_locations = list(pyautogui.locateAllOnScreen(
                screenshot, 
                confidence=0.7,
                grayscale=True
            ))
            
            if play_locations:
                print(f"✅ Найдено {len(play_locations)} возможных кнопок Play")
                for i, location in enumerate(play_locations):
                    print(f"  {i}: {pyautogui.center(location)}")
            else:
                print("❌ Кнопки Play не найдены через locateAllOnScreen")
                
        except Exception as e:
            print(f"❌ Ошибка поиска через изображение: {e}")
        
        print("\n🔍 Пробуем альтернативные методы...")
        
        # Альтернатива 1: Поиск по пикселю
        print("1️⃣ Поиск характерных цветов кнопки Play...")
        
        # Типичные координаты для кнопки Play в браузере (нижняя часть)
        play_candidates = [
            (960, 950),   # Центр низа экрана
            (100, 950),   # Левый угол низа
            (300, 950),   # Левая часть низа
            (1820, 950),  # Правый угол низа
        ]
        
        for x, y in play_candidates:
            if x < screenshot.size[0] and y < screenshot.size[1]:
                pixel_color = screenshot.getpixel((x, y))
                print(f"  Координаты ({x}, {y}): цвет {pixel_color}")
        
        # Альтернатива 2: Поиск кнопки по области
        print("2️⃣ Поиск в нижней трети экрана...")
        
        width, height = screenshot.size
        bottom_third_y = height * 2 // 3
        
        print(f"  Экран: {width}x{height}")
        print(f"  Ищем в области от y={bottom_third_y} до y={height}")
        
        # Альтернатива 3: Прямой клик по известным координатам из лога
        print("3️⃣ Используем координаты из лога Open Interpreter...")
        known_coordinates = [
            (318, 451),   # Из лога: множественные найденные кнопки Play
            (260, 480),
            (312, 683),
            (1776, 766)
        ]
        
        for i, (x, y) in enumerate(known_coordinates):
            if x < width and y < height:
                pixel = screenshot.getpixel((x, y))
                print(f"  Координата {i+1}: ({x}, {y}) цвет={pixel}")
                
                # ТЕСТ-КЛИК (без реального клика, только проверка)
                print(f"    ✅ Готов к клику по ({x}, {y})")
            else:
                print(f"  Координата {i+1}: ({x}, {y}) - вне экрана")
        
        return True
        
    except Exception as e:
        print(f"❌ Общая ошибка теста: {e}")
        return False

def smart_play_click():
    """Умный клик по кнопке Play"""
    try:
        print("\n🎯 ПРОБУЕМ РЕАЛЬНЫЙ КЛИК ПО КНОПКЕ PLAY...")
        
        # Используем координаты из успешного поиска Open Interpreter
        best_coordinates = [
            (318, 451),   # Первая найденная кнопка
            (260, 480),   # Вторая найденная кнопка
        ]
        
        for i, (x, y) in enumerate(best_coordinates):
            print(f"🖱️ Пробуем клик {i+1}: ({x}, {y})")
            
            # Проверяем, что координаты в пределах экрана
            screen_width, screen_height = pyautogui.size()
            if 0 <= x <= screen_width and 0 <= y <= screen_height:
                
                # РЕАЛЬНЫЙ КЛИК!
                pyautogui.click(x, y)
                print(f"✅ Клик выполнен по ({x}, {y})")
                
                time.sleep(1)  # Пауза между кликами
                
                return True
            else:
                print(f"❌ Координаты ({x}, {y}) вне экрана {screen_width}x{screen_height}")
        
        return False
        
    except Exception as e:
        print(f"❌ Ошибка клика: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Запуск теста кнопки Play...")
    
    # Фаза 1: Анализ
    success = simple_play_test()
    
    if success:
        # Фаза 2: Попытка клика (только если пользователь согласен)
        response = input("\n❓ Попробовать реальный клик по кнопке Play? (y/n): ")
        if response.lower() == 'y':
            smart_play_click()
        else:
            print("👍 Тест завершен без клика")
    
    print("\n🏁 Тест завершен!")
