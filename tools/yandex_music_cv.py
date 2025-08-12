#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 Яндекс Музыка CV навыки для Open Interpreter
Специальные навыки для работы с Яндекс.Музыка через компьютерное зрение
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from enhanced_cv import enhanced_cv
import time
import webbrowser
import logging

logger = logging.getLogger(__name__)

class YandexMusicCV:
    """Контроллер Яндекс Музыки с компьютерным зрением"""
    
    def __init__(self):
        self.cv = enhanced_cv
        self.yandex_music_url = "https://music.yandex.ru"
        logger.info("🎵 YandexMusicCV инициализирован")
    
    def open_and_play_yandex_music(self, search_query: str = None) -> str:
        """
        Открыть Яндекс Музыку и начать воспроизведение
        """
        try:
            logger.info(f"🎵 Открываем Яндекс Музыку: {search_query or 'любая музыка'}")
            
            # 1. Открыть Яндекс Музыку в браузере
            if search_query:
                search_url = f"{self.yandex_music_url}/search?text={search_query.replace(' ', '%20')}"
                webbrowser.open(search_url)
            else:
                webbrowser.open(self.yandex_music_url)
            
            # 2. Подождать загрузки страницы
            time.sleep(4)
            
            # 3. Попробовать найти и кликнуть кнопку воспроизведения
            play_attempts = [
                "кнопка воспроизведения",
                "play button", 
                "кнопка плей",
                "▶️",
                "треугольник воспроизведения"
            ]
            
            for attempt in play_attempts:
                result = self.cv.find_and_click(attempt, click=True)
                if result['success']:
                    logger.info(f"✅ Нашли и кликнули: {attempt}")
                    time.sleep(1)
                    return f"🎵 Яндекс Музыка запущена! Играет: {search_query or 'рекомендации'}"
                
                time.sleep(0.5)
            
            # 4. Если кнопка Play не найдена, попробовать кликнуть по первому треку
            track_attempts = [
                "первый трек в списке",
                "название песни",
                "трек для воспроизведения"
            ]
            
            for attempt in track_attempts:
                result = self.cv.find_and_click(attempt, click=True)
                if result['success']:
                    logger.info(f"✅ Кликнули по треку: {attempt}")
                    return f"🎵 Яндекс Музыка: трек запущен! {search_query or ''}"
                
                time.sleep(0.5)
            
            # 5. Если ничего не сработало, попробовать нажать пробел
            import pyautogui
            pyautogui.press('space')
            
            return f"🎵 Яндекс Музыка открыта. Попробовали запустить воспроизведение через пробел."
            
        except Exception as e:
            logger.error(f"❌ Ошибка управления Яндекс Музыкой: {e}")
            return f"❌ Ошибка: {e}"
    
    def pause_yandex_music(self) -> str:
        """Пауза в Яндекс Музыке"""
        try:
            # Попробовать найти кнопку паузы
            pause_result = self.cv.find_and_click("кнопка паузы", click=True)
            if pause_result['success']:
                return "⏸️ Музыка поставлена на паузу"
            
            # Если не нашли, нажать пробел
            import pyautogui
            pyautogui.press('space')
            return "⏸️ Отправлена команда паузы (пробел)"
            
        except Exception as e:
            return f"❌ Ошибка паузы: {e}"
    
    def next_track(self) -> str:
        """Следующий трек"""
        try:
            next_result = self.cv.find_and_click("следующий трек", click=True)
            if next_result['success']:
                return "⏭️ Переключено на следующий трек"
            
            # Попробовать стрелку вправо
            import pyautogui
            pyautogui.press('right')
            return "⏭️ Отправлена команда следующего трека"
            
        except Exception as e:
            return f"❌ Ошибка переключения: {e}"
    
    def analyze_yandex_music_screen(self) -> str:
        """Анализ экрана Яндекс Музыки"""
        try:
            result = self.cv.smart_screenshot_analysis()
            if result['success']:
                return f"📊 Анализ экрана Яндекс Музыки: найдено {result['elements_count']} элементов интерфейса"
            else:
                return f"❌ Ошибка анализа: {result['error']}"
        except Exception as e:
            return f"❌ Ошибка: {e}"

# Глобальный экземпляр
yandex_music_cv = YandexMusicCV()

# Функции для интеграции с Open Interpreter
def play_yandex_music_with_cv(query: str = None) -> str:
    """
    Запустить Яндекс Музыку с компьютерным зрением
    
    Args:
        query: Что искать (опционально)
    
    Returns:
        Результат выполнения
    """
    return yandex_music_cv.open_and_play_yandex_music(query)

def pause_yandex_music_cv() -> str:
    """Пауза в Яндекс Музыке через CV"""
    return yandex_music_cv.pause_yandex_music()

def next_track_yandex_cv() -> str:
    """Следующий трек в Яндекс Музыке через CV"""
    return yandex_music_cv.next_track()

def analyze_yandex_music_cv() -> str:
    """Анализ экрана Яндекс Музыки"""
    return yandex_music_cv.analyze_yandex_music_screen()

if __name__ == "__main__":
    # Тест навыка
    print("🧪 Тестирование Яндекс Музыка CV...")
    
    result = analyze_yandex_music_cv()
    print(f"Анализ: {result}")
