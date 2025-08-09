#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Утилиты для автоматизации GUI приложений
"""

import pyautogui
import pygetwindow as gw
import subprocess
import time
import os
import psutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Настройка pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

class VSCodeAutomation:
    """Автоматизация Visual Studio Code"""
    
    @staticmethod
    def open_vscode(file_path=None):
        """Открыть VS Code с опциональным файлом"""
        try:
            if file_path:
                subprocess.run(['code', file_path], check=True)
            else:
                subprocess.run(['code'], check=True)
            time.sleep(2)  # Ждем загрузки
            return True
        except Exception as e:
            print(f"Ошибка открытия VS Code: {e}")
            return False
    
    @staticmethod
    def find_vscode_window():
        """Найти окно VS Code"""
        try:
            windows = gw.getWindowsWithTitle('Visual Studio Code')
            if windows:
                return windows[0]
            # Попробуем найти по части названия
            all_windows = gw.getAllWindows()
            for window in all_windows:
                if 'Visual Studio Code' in window.title or 'Code' in window.title:
                    return window
            return None
        except Exception as e:
            print(f"Ошибка поиска окна VS Code: {e}")
            return None
    
    @staticmethod
    def focus_vscode():
        """Сфокусироваться на окне VS Code"""
        try:
            window = VSCodeAutomation.find_vscode_window()
            if window:
                window.activate()
                time.sleep(0.5)
                return True
            return False
        except Exception as e:
            print(f"Ошибка фокусировки VS Code: {e}")
            return False
    
    @staticmethod
    def edit_file(file_path, new_content):
        """Редактировать файл в VS Code"""
        try:
            # Открываем файл в VS Code
            VSCodeAutomation.open_vscode(file_path)
            time.sleep(2)
            
            # Выделяем весь текст
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.5)
            
            # Вставляем новый контент
            pyautogui.typewrite(new_content)
            time.sleep(0.5)
            
            # Сохраняем
            pyautogui.hotkey('ctrl', 's')
            time.sleep(0.5)
            
            return True
        except Exception as e:
            print(f"Ошибка редактирования файла: {e}")
            return False

class BrowserAutomation:
    """Автоматизация браузера"""
    
    def __init__(self):
        self.driver = None
    
    def connect_to_existing_chrome(self):
        """Подключиться к существующему экземпляру Chrome"""
        try:
            # Настройки для подключения к существующему Chrome
            chrome_options = Options()
            chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except Exception as e:
            print(f"Не удалось подключиться к Chrome: {e}")
            print("Убедитесь, что Chrome запущен с флагом --remote-debugging-port=9222")
            return False
    
    def start_chrome_with_debugging(self):
        """Запустить Chrome с отладочным портом"""
        try:
            # Закрываем все процессы Chrome
            for proc in psutil.process_iter(['pid', 'name']):
                if 'chrome' in proc.info['name'].lower():
                    proc.terminate()
            
            time.sleep(2)
            
            # Запускаем Chrome с отладочным портом
            chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            if not os.path.exists(chrome_path):
                chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            
            subprocess.Popen([
                chrome_path,
                "--remote-debugging-port=9222",
                "--user-data-dir=C:\\temp\\chrome_debug"
            ])
            
            time.sleep(3)
            
            # Подключаемся
            return self.connect_to_existing_chrome()
        except Exception as e:
            print(f"Ошибка запуска Chrome: {e}")
            return False
    
    def get_all_tabs(self):
        """Получить информацию о всех вкладках"""
        try:
            if not self.driver:
                return []
            
            tabs = []
            original_window = self.driver.current_window_handle
            
            for window_handle in self.driver.window_handles:
                self.driver.switch_to.window(window_handle)
                tabs.append({
                    'title': self.driver.title,
                    'url': self.driver.current_url,
                    'handle': window_handle
                })
            
            # Возвращаемся к исходной вкладке
            self.driver.switch_to.window(original_window)
            return tabs
        except Exception as e:
            print(f"Ошибка получения вкладок: {e}")
            return []
    
    def get_page_content(self, include_text=True, include_links=True):
        """Получить содержимое текущей страницы"""
        try:
            if not self.driver:
                return None
            
            content = {
                'title': self.driver.title,
                'url': self.driver.current_url
            }
            
            if include_text:
                content['text'] = self.driver.find_element(By.TAG_NAME, 'body').text
            
            if include_links:
                links = self.driver.find_elements(By.TAG_NAME, 'a')
                content['links'] = [{'text': link.text, 'href': link.get_attribute('href')} 
                                  for link in links if link.get_attribute('href')]
            
            return content
        except Exception as e:
            print(f"Ошибка получения содержимого страницы: {e}")
            return None
    
    def close(self):
        """Закрыть драйвер"""
        if self.driver:
            self.driver.quit()
            self.driver = None

class ScreenAutomation:
    """Автоматизация экрана"""
    
    @staticmethod
    def take_screenshot(save_path=None):
        """Сделать скриншот"""
        try:
            screenshot = pyautogui.screenshot()
            if save_path:
                screenshot.save(save_path)
            return screenshot
        except Exception as e:
            print(f"Ошибка создания скриншота: {e}")
            return None
    
    @staticmethod
    def find_and_click(image_path, confidence=0.8):
        """Найти изображение на экране и кликнуть по нему"""
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                pyautogui.click(center)
                return True
            return False
        except Exception as e:
            print(f"Ошибка поиска и клика по изображению: {e}")
            return False
    
    @staticmethod
    def get_screen_size():
        """Получить размер экрана"""
        return pyautogui.size()

# Глобальные экземпляры для использования
vscode = VSCodeAutomation()
browser = BrowserAutomation()
screen = ScreenAutomation()
