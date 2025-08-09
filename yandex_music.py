#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Система управления Яндекс.Музыкой и браузерной музыкой
"""

import time
import json
import os
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    import pyautogui
    import pygetwindow as gw
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    import undetected_chromedriver as uc
    WEB_AUTOMATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Веб-автоматизация недоступна: {e}")
    WEB_AUTOMATION_AVAILABLE = False

try:
    import psutil
    PROCESS_CONTROL_AVAILABLE = True
except ImportError:
    PROCESS_CONTROL_AVAILABLE = False

class YandexMusicController:
    """Контроллер для управления Яндекс.Музыкой"""
    
    def __init__(self):
        self.driver = None
        self.music_window = None
        
        # Селекторы для Яндекс.Музыки
        self.selectors = {
            'play_button': '[class*="play"], [aria-label*="Воспроизвести"], [title*="Воспроизвести"]',
            'pause_button': '[class*="pause"], [aria-label*="Пауза"], [title*="Пауза"]',
            'next_button': '[class*="next"], [aria-label*="Следующий"], [title*="Следующий"]',
            'prev_button': '[class*="prev"], [aria-label*="Предыдущий"], [title*="Предыдущий"]',
            'search_input': 'input[placeholder*="Найти"], input[aria-label*="Поиск"], .search__input',
            'volume_control': '[class*="volume"], [aria-label*="Громкость"]',
            'player_controls': '.player-controls, .player, [class*="player"]'
        }
        
        # URL'ы сервисов
        self.music_services = {
            'yandex': 'https://music.yandex.ru',
            'youtube_music': 'https://music.youtube.com',
            'spotify_web': 'https://open.spotify.com',
            'vk_music': 'https://vk.com/audio'
        }
    
    def find_browser_with_music(self) -> Optional[str]:
        """Находит браузер с открытой музыкой"""
        music_keywords = ['яндекс.музыка', 'yandex music', 'spotify', 'youtube music', 'music.yandex', 'music.youtube']
        
        try:
            windows = gw.getAllWindows()
            for window in windows:
                title = window.title.lower()
                for keyword in music_keywords:
                    if keyword in title:
                        print(f"🎵 Найдено окно с музыкой: {window.title}")
                        return window.title
        except Exception as e:
            print(f"⚠️ Ошибка поиска окон: {e}")
        
        return None
    
    def activate_music_window(self) -> bool:
        """Активирует окно с музыкой"""
        try:
            music_title = self.find_browser_with_music()
            if music_title:
                windows = gw.getWindowsWithTitle(music_title)
                if windows:
                    window = windows[0]
                    window.activate()
                    time.sleep(1)
                    return True
        except Exception as e:
            print(f"⚠️ Ошибка активации окна: {e}")
        
        return False
    
    def open_yandex_music(self, headless: bool = False) -> bool:
        """Открывает Яндекс.Музыку в браузере"""
        if not WEB_AUTOMATION_AVAILABLE:
            return self._open_with_browser()
        
        try:
            # Настройки Chrome
            options = Options()
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            # Пытаемся использовать undetected-chromedriver
            try:
                self.driver = uc.Chrome(options=options)
            except:
                # Fallback на обычный Chrome
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            
            print("🎵 Открываю Яндекс.Музыку...")
            self.driver.get(self.music_services['yandex'])
            
            # Ждем загрузки страницы
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ Яндекс.Музыка открыта")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка открытия Яндекс.Музыки: {e}")
            return self._open_with_browser()
    
    def _open_with_browser(self) -> bool:
        """Открывает музыку в браузере по умолчанию"""
        try:
            import webbrowser
            webbrowser.open(self.music_services['yandex'])
            time.sleep(3)
            print("✅ Яндекс.Музыка открыта в браузере по умолчанию")
            return True
        except Exception as e:
            print(f"❌ Ошибка открытия в браузере: {e}")
            return False
    
    def control_playback(self, action: str) -> str:
        """Управляет воспроизведением"""
        # Сначала пробуем горячие клавиши
        keyboard_result = self._try_keyboard_control(action)
        if "успешно" in keyboard_result.lower():
            return keyboard_result
        
        # Затем пробуем через активацию окна
        window_result = self._try_window_control(action)
        if "успешно" in window_result.lower():
            return window_result
        
        # В конце пробуем через Selenium
        if self.driver:
            return self._try_selenium_control(action)
        
        return f"❌ Не удалось выполнить действие: {action}"
    
    def _try_keyboard_control(self, action: str) -> str:
        """Пытается управлять через клавиатуру"""
        try:
            # Медиа клавиши
            media_keys = {
                'play': 'playpause',
                'pause': 'playpause',
                'next': 'nexttrack',
                'previous': 'prevtrack',
                'volume_up': 'volumeup',
                'volume_down': 'volumedown'
            }
            
            if action in media_keys:
                print(f"🎹 Нажимаю медиа клавишу: {media_keys[action]}")
                pyautogui.press(media_keys[action])
                time.sleep(0.5)
                return f"✅ Медиа команда '{action}' выполнена успешно"
            
            return f"❌ Неизвестная команда: {action}"
            
        except Exception as e:
            return f"❌ Ошибка клавиатурного управления: {e}"
    
    def _try_window_control(self, action: str) -> str:
        """Пытается управлять через активацию окна и клавиши"""
        try:
            if not self.activate_music_window():
                return "❌ Не найдено окно с музыкой"
            
            # Горячие клавиши для браузера
            browser_keys = {
                'play': 'space',
                'pause': 'space',
                'next': ['shift', 'n'],
                'previous': ['shift', 'p'],
                'volume_up': ['shift', 'up'],
                'volume_down': ['shift', 'down']
            }
            
            if action in browser_keys:
                keys = browser_keys[action]
                if isinstance(keys, list):
                    pyautogui.hotkey(*keys)
                else:
                    pyautogui.press(keys)
                
                return f"✅ Команда '{action}' выполнена в окне браузера"
            
            return f"❌ Неизвестная команда: {action}"
            
        except Exception as e:
            return f"❌ Ошибка управления окном: {e}"
    
    def _try_selenium_control(self, action: str) -> str:
        """Пытается управлять через Selenium"""
        try:
            if not self.driver:
                return "❌ Драйвер браузера не инициализирован"
            
            # Ищем кнопки управления
            if action in ['play', 'pause']:
                # Пробуем найти кнопку воспроизведения/паузы
                selectors_to_try = [
                    self.selectors['play_button'],
                    self.selectors['pause_button'],
                    '.player__play, .play-button, [data-testid="play-button"]'
                ]
                
                for selector in selectors_to_try:
                    try:
                        element = WebDriverWait(self.driver, 2).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        element.click()
                        return f"✅ Кнопка '{action}' нажата через браузер"
                    except:
                        continue
            
            elif action == 'next':
                try:
                    element = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.selectors['next_button']))
                    )
                    element.click()
                    return "✅ Переключено на следующий трек"
                except:
                    pass
            
            elif action == 'previous':
                try:
                    element = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, self.selectors['prev_button']))
                    )
                    element.click()
                    return "✅ Переключено на предыдущий трек"
                except:
                    pass
            
            # Если кнопки не найдены, пробуем клавиши
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)
            return f"✅ Отправлен пробел для '{action}'"
            
        except Exception as e:
            return f"❌ Ошибка Selenium управления: {e}"
    
    def search_and_play(self, query: str) -> str:
        """Ищет и воспроизводит музыку"""
        try:
            if not self.driver:
                if not self.open_yandex_music():
                    return "❌ Не удалось открыть Яндекс.Музыку"
            
            # Ищем поле поиска
            search_input = None
            search_selectors = [
                'input[placeholder*="Найти"]',
                'input[placeholder*="Поиск"]',
                '.search__input',
                '[data-testid="search-input"]',
                'input[type="search"]'
            ]
            
            for selector in search_selectors:
                try:
                    search_input = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not search_input:
                return "❌ Не найдено поле поиска"
            
            # Вводим запрос
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
            
            time.sleep(2)
            
            # Пытаемся нажать на первый результат
            play_selectors = [
                '.track__play',
                '.play-button',
                '[data-testid="play-button"]',
                '.d-track__play'
            ]
            
            for selector in play_selectors:
                try:
                    play_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    play_button.click()
                    return f"✅ Воспроизведение '{query}' запущено"
                except:
                    continue
            
            return f"✅ Поиск '{query}' выполнен, попробуйте нажать play"
            
        except Exception as e:
            return f"❌ Ошибка поиска и воспроизведения: {e}"
    
    def get_current_track(self) -> str:
        """Получает информацию о текущем треке"""
        try:
            if not self.driver:
                return "❌ Браузер не открыт"
            
            # Селекторы для информации о треке
            title_selectors = [
                '.track__title',
                '.d-track__name',
                '[data-testid="track-title"]'
            ]
            
            artist_selectors = [
                '.track__artists',
                '.d-track__artists',
                '[data-testid="track-artist"]'
            ]
            
            title = "Неизвестно"
            artist = "Неизвестно"
            
            for selector in title_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    title = element.text
                    break
                except:
                    continue
            
            for selector in artist_selectors:
                try:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    artist = element.text
                    break
                except:
                    continue
            
            return f"🎵 Сейчас играет: {artist} - {title}"
            
        except Exception as e:
            return f"❌ Ошибка получения информации о треке: {e}"
    
    def close_browser(self):
        """Закрывает браузер"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                print("✅ Браузер закрыт")
        except Exception as e:
            print(f"⚠️ Ошибка закрытия браузера: {e}")

# Глобальный контроллер музыки
yandex_music = YandexMusicController()

# Функции для интеграции с Open Interpreter
def play_yandex_music(query: str = None) -> str:
    """Воспроизводит музыку в Яндекс.Музыке"""
    if query:
        return yandex_music.search_and_play(query)
    else:
        return yandex_music.control_playback('play')

def pause_yandex_music() -> str:
    """Ставит музыку на паузу"""
    return yandex_music.control_playback('pause')

def next_track_yandex() -> str:
    """Переключает на следующий трек"""
    return yandex_music.control_playback('next')

def previous_track_yandex() -> str:
    """Переключает на предыдущий трек"""
    return yandex_music.control_playback('previous')

def open_yandex_music_browser() -> str:
    """Открывает Яндекс.Музыку в браузере"""
    if yandex_music.open_yandex_music():
        return "✅ Яндекс.Музыка открыта"
    else:
        return "❌ Не удалось открыть Яндекс.Музыку"

def get_current_track_info() -> str:
    """Получает информацию о текущем треке"""
    return yandex_music.get_current_track()

def smart_music_control(action: str, query: str = None) -> str:
    """Умное управление музыкой"""
    action = action.lower()
    
    if action in ['включи', 'play', 'воспроизведи']:
        if query:
            return play_yandex_music(query)
        else:
            return yandex_music.control_playback('play')
    
    elif action in ['пауза', 'pause', 'стоп', 'stop']:
        return pause_yandex_music()
    
    elif action in ['следующий', 'next', 'дальше']:
        return next_track_yandex()
    
    elif action in ['предыдущий', 'previous', 'назад']:
        return previous_track_yandex()
    
    elif action in ['открой', 'open', 'запусти']:
        return open_yandex_music_browser()
    
    elif action in ['что играет', 'current', 'трек']:
        return get_current_track_info()
    
    else:
        return f"❌ Неизвестная команда: {action}"
