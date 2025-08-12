#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 CV Navigation Skills для Open Interpreter
Навыки навигации и взаимодействия с компьютером
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_cv import enhanced_cv, smart_click, analyze_screen
import time
import logging

logger = logging.getLogger(__name__)

class CVNavigationSkills:
    """Навыки навигации с помощью компьютерного зрения"""
    
    def __init__(self):
        self.cv = enhanced_cv
        logger.info("🎯 CV Navigation Skills инициализированы")
    
    def find_and_open_program(self, program_name: str) -> str:
        """Найти и открыть программу"""
        try:
            # 1. Анализ текущего экрана
            screen_analysis = self.cv.smart_screenshot_analysis()
            
            if not screen_analysis['success']:
                return f"❌ Не удалось проанализировать экран: {screen_analysis['error']}"
            
            # 2. Поиск иконки программы или ярлыка
            result = self.cv.find_and_click(f"иконка {program_name}", click=True)
            
            if result['success']:
                return f"✅ Программа '{program_name}' запущена успешно"
            else:
                # 3. Попробовать через меню Пуск
                return self._open_via_start_menu(program_name)
                
        except Exception as e:
            logger.error(f"❌ Ошибка запуска программы: {e}")
            return f"❌ Ошибка: {e}"
    
    def _open_via_start_menu(self, program_name: str) -> str:
        """Открытие через меню Пуск"""
        try:
            import pyautogui
            
            # Нажать Win
            pyautogui.press('win')
            time.sleep(0.5)
            
            # Ввести название программы
            pyautogui.typewrite(program_name)
            time.sleep(0.3)
            
            # Enter для запуска
            pyautogui.press('enter')
            
            return f"✅ Попытка запуска '{program_name}' через меню Пуск"
            
        except Exception as e:
            return f"❌ Ошибка работы с меню Пуск: {e}"
    
    def click_on_text(self, text_content: str) -> str:
        """Кликнуть по тексту на экране"""
        try:
            result = self.cv.find_and_click(f"текст {text_content}", click=True)
            
            if result['success']:
                return f"✅ Клик по тексту '{text_content}' выполнен"
            else:
                return f"❌ Текст '{text_content}' не найден: {result['error']}"
                
        except Exception as e:
            return f"❌ Ошибка клика по тексту: {e}"
    
    def click_on_button(self, button_description: str) -> str:
        """Кликнуть по кнопке"""
        try:
            result = self.cv.find_and_click(f"кнопка {button_description}", click=True)
            
            if result['success']:
                return f"✅ Клик по кнопке '{button_description}' выполнен"
            else:
                return f"❌ Кнопка '{button_description}' не найдена: {result['error']}"
                
        except Exception as e:
            return f"❌ Ошибка клика по кнопке: {e}"
    
    def navigate_to_element(self, element_description: str, action: str = "click") -> str:
        """Универсальная навигация к элементу"""
        try:
            # Анализ экрана
            screen_info = analyze_screen()
            
            # Поиск элемента
            if action == "click":
                result = smart_click(element_description)
            else:
                # Другие действия могут быть добавлены
                result = f"🔄 Действие '{action}' пока не поддерживается"
            
            return f"📍 Навигация: {result}"
            
        except Exception as e:
            return f"❌ Ошибка навигации: {e}"
    
    def take_smart_screenshot(self, filename: str = None) -> str:
        """Умный скриншот с анализом"""
        try:
            if not filename:
                timestamp = int(time.time())
                filename = f"smart_screenshot_{timestamp}.png"
            
            # Путь сохранения
            save_path = os.path.join(os.getcwd(), filename)
            
            result = self.cv.smart_screenshot_analysis(save_path)
            
            if result['success']:
                return f"📸 Умный скриншот сохранен: {filename}\n🔍 Найдено элементов: {result['elements_count']}"
            else:
                return f"❌ Ошибка создания скриншота: {result['error']}"
                
        except Exception as e:
            return f"❌ Ошибка: {e}"

# Глобальный экземпляр навыков
cv_skills = CVNavigationSkills()

# Функции для интеграции с Open Interpreter навыками
def open_program(program_name: str) -> str:
    """
    Открыть программу по названию
    
    Args:
        program_name: Название программы (например, "браузер", "блокнот", "калькулятор")
    
    Returns:
        Результат выполнения
    """
    return cv_skills.find_and_open_program(program_name)

def click_text(text: str) -> str:
    """
    Кликнуть по тексту на экране
    
    Args:
        text: Текст для поиска и клика
    
    Returns:
        Результат выполнения
    """
    return cv_skills.click_on_text(text)

def click_button(button_name: str) -> str:
    """
    Кликнуть по кнопке
    
    Args:
        button_name: Описание кнопки (например, "ОК", "Отмена", "Сохранить")
    
    Returns:
        Результат выполнения
    """
    return cv_skills.click_on_button(button_name)

def navigate_to(element: str, action: str = "click") -> str:
    """
    Навигация к элементу интерфейса
    
    Args:
        element: Описание элемента
        action: Действие ("click", "hover", etc.)
    
    Returns:
        Результат выполнения
    """
    return cv_skills.navigate_to_element(element, action)

def smart_screenshot(filename: str = None) -> str:
    """
    Создать умный скриншот с анализом UI элементов
    
    Args:
        filename: Имя файла (опционально)
    
    Returns:
        Результат выполнения
    """
    return cv_skills.take_smart_screenshot(filename)

def screen_analysis() -> str:
    """
    Анализ текущего экрана
    
    Returns:
        Информация об элементах на экране
    """
    return analyze_screen()

# Музыкальные навыки с CV поддержкой
def play_music_smart(song_request: str = None) -> str:
    """
    Умное воспроизведение музыки с компьютерным зрением
    """
    try:
        # 1. Попробовать открыть медиаплеер
        media_player_result = cv_skills.find_and_open_program("медиаплеер")
        
        if "успешно" not in media_player_result.lower():
            # Попробовать другие варианты
            for player in ["VLC", "Windows Media Player", "музыка", "плеер"]:
                result = cv_skills.find_and_open_program(player)
                if "успешно" in result.lower():
                    break
        
        time.sleep(2)  # Ждем загрузки плеера
        
        # 2. Если есть запрос на конкретную песню
        if song_request:
            # Поиск поля поиска
            search_result = cv_skills.click_on_text("поиск")
            if "выполнен" not in search_result:
                # Попробовать Ctrl+F
                import pyautogui
                pyautogui.hotkey('ctrl', 'f')
                time.sleep(0.5)
            
            # Ввод запроса
            import pyautogui
            pyautogui.typewrite(song_request)
            pyautogui.press('enter')
        
        # 3. Найти и нажать кнопку воспроизведения
        play_result = cv_skills.click_on_button("воспроизведение")
        if "выполнен" not in play_result:
            # Попробовать пробел
            import pyautogui
            pyautogui.press('space')
        
        return f"🎵 Музыка запущена! {song_request if song_request else 'Плейлист'}"
        
    except Exception as e:
        logger.error(f"❌ Ошибка воспроизведения музыки: {e}")
        return f"❌ Ошибка: {e}"

if __name__ == "__main__":
    # Тест навыков
    print("🧪 Тестирование CV Navigation Skills...")
    
    # Тест анализа экрана
    result = screen_analysis()
    print(f"Анализ экрана: {result}")
    
    # Тест скриншота
    screenshot_result = smart_screenshot("test_cv_skills.png")
    print(f"Скриншот: {screenshot_result}")
