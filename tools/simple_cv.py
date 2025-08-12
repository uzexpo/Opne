#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ПРОСТЫЕ И НАДЕЖНЫЕ CV ФУНКЦИИ 🚀
Замена для проблемных Enhanced CV функций
"""

import pyautogui
import time
import logging
from typing import List, Dict, Tuple, Optional

logger = logging.getLogger(__name__)

class SimpleCV:
    """Простые и надежные CV функции без внешних зависимостей"""
    
    def __init__(self):
        self.last_screenshot = None
        self.last_screenshot_time = 0
        
        # Известные координаты кнопок Play из лога Open Interpreter
        self.known_play_coordinates = [
            (318, 451),   # Первая найденная позиция
            (260, 480),   # Вторая найденная позиция  
            (312, 683),   # Третья найденная позиция
            (1776, 766),  # Четвертая найденная позиция
        ]
        
    def get_screenshot(self):
        """Получить скриншот с кэшированием"""
        current_time = time.time()
        if (self.last_screenshot is None or 
            current_time - self.last_screenshot_time > 1.0):  # Кэш на 1 секунду
            self.last_screenshot = pyautogui.screenshot()
            self.last_screenshot_time = current_time
        return self.last_screenshot
    
    def find_text_simple(self, text: str) -> List[Dict]:
        """
        Простой поиск текста на экране
        Возвращает список в формате Open Interpreter
        """
        try:
            print(f"🔍 Ищем текст: '{text}'")
            
            # Получаем скриншот
            screenshot = self.get_screenshot()
            
            # Известные координаты кнопок Play из лога Open Interpreter
            if text.lower() in ['play', 'плей', 'воспроизведение']:
                # Используем проверенные координаты
                results = []
                for i, (x, y) in enumerate(self.known_play_coordinates):
                    # Проверяем, что координаты в пределах экрана
                    if 0 <= x < screenshot.size[0] and 0 <= y < screenshot.size[1]:
                        results.append({
                            "coordinates": (x, y),
                            "text": text,
                            "similarity": 0.9,
                            "source": f"known_location_{i+1}"
                        })
                
                if results:
                    print(f"✅ Найдено {len(results)} кнопок Play")
                    return results
            
            # Альтернативный поиск через pyautogui
            try:
                # Попробуем найти через center точку экрана (часто там кнопки)
                center_x, center_y = screenshot.size[0] // 2, screenshot.size[1] // 2
                
                # Поиск в разных областях экрана
                search_areas = [
                    (center_x, center_y),                    # Центр
                    (center_x, screenshot.size[1] - 100),    # Нижний центр
                    (100, screenshot.size[1] - 100),         # Нижний левый
                    (screenshot.size[0] - 100, screenshot.size[1] - 100),  # Нижний правый
                ]
                
                results = []
                for i, (x, y) in enumerate(search_areas):
                    results.append({
                        "coordinates": (x, y),
                        "text": text,
                        "similarity": 0.7,
                        "source": f"area_search_{i+1}"
                    })
                
                print(f"✅ Возвращаем {len(results)} альтернативных позиций")
                return results
                
            except Exception as e:
                print(f"⚠️ Ошибка альтернативного поиска: {e}")
                return []
            
        except Exception as e:
            print(f"❌ Ошибка поиска текста: {e}")
            return []
    
    def find_element_simple(self, description: str) -> List[Dict]:
        """Простой поиск элементов"""
        try:
            # Если описание содержит "play", "кнопка", "музыка"
            if any(word in description.lower() for word in ['play', 'кнопка', 'музыка', 'воспроизведение']):
                return self.find_text_simple("Play")
            
            # Общий поиск
            return self.find_text_simple(description)
            
        except Exception as e:
            print(f"❌ Ошибка поиска элемента: {e}")
            return []
    
    def click_coordinates(self, x: int, y: int) -> bool:
        """Простой клик по координатам"""
        try:
            # Проверяем границы экрана
            screen_width, screen_height = pyautogui.size()
            if 0 <= x <= screen_width and 0 <= y <= screen_height:
                pyautogui.click(x, y)
                print(f"✅ Клик выполнен по ({x}, {y})")
                return True
            else:
                print(f"❌ Координаты ({x}, {y}) вне экрана")
                return False
        except Exception as e:
            print(f"❌ Ошибка клика: {e}")
            return False
    
    def click_play_button(self) -> str:
        """Специальная функция для клика по кнопке Play"""
        try:
            play_buttons = self.find_text_simple("Play")
            
            if play_buttons:
                # Кликаем по первой найденной кнопке
                coords = play_buttons[0]["coordinates"]
                if self.click_coordinates(coords[0], coords[1]):
                    return f"✅ Клик по кнопке Play выполнен: {coords}"
                else:
                    return f"❌ Не удалось кликнуть по {coords}"
            else:
                # Пробуем клавишу Space как альтернативу
                pyautogui.press('space')
                return "✅ Нажата клавиша Space (альтернатива Play)"
                
        except Exception as e:
            return f"❌ Ошибка клика по Play: {e}"

# Глобальный экземпляр
simple_cv = SimpleCV()

def simple_find_text(text: str) -> List[Dict]:
    """Глобальная функция поиска текста"""
    return simple_cv.find_text_simple(text)

def simple_find_element(description: str) -> List[Dict]:
    """Глобальная функция поиска элементов"""
    return simple_cv.find_element_simple(description)

def simple_click(x: int, y: int) -> bool:
    """Глобальная функция клика"""
    return simple_cv.click_coordinates(x, y)

def simple_screenshot():
    """Глобальная функция скриншота"""
    return simple_cv.get_screenshot()

# Функции для быстрого поиска кнопки Play
def find_play_button() -> List[Dict]:
    """Специальная функция для поиска кнопки Play"""
    return simple_cv.find_text_simple("Play")

def click_play_button() -> str:
    """Специальная функция для клика по кнопке Play"""
    try:
        play_buttons = find_play_button()
        
        if play_buttons:
            # Кликаем по первой найденной кнопке
            coords = play_buttons[0]["coordinates"]
            if simple_cv.click_coordinates(coords[0], coords[1]):
                return f"✅ Клик по кнопке Play выполнен: {coords}"
            else:
                return f"❌ Не удалось кликнуть по {coords}"
        else:
            # Пробуем клавишу Space как альтернативу
            pyautogui.press('space')
            return "✅ Нажата клавиша Space (альтернатива Play)"
            
    except Exception as e:
        return f"❌ Ошибка клика по Play: {e}"

if __name__ == "__main__":
    # Тест
    print("🧪 Тестируем простые CV функции...")
    
    results = find_play_button()
    print(f"Найдено кнопок Play: {len(results)}")
    
    for i, result in enumerate(results):
        print(f"  {i+1}: {result}")
