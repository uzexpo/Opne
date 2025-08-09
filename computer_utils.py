#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Утилиты для расширенной работы Open Interpreter с компьютером
"""

import os
import sys
import time
import subprocess
import psutil
import json
from pathlib import Path

# Импортируем GUI библиотеки
try:
    import pyautogui
    import cv2
    import numpy as np
    from PIL import Image
    GUI_AVAILABLE = True
    # Настройки pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3
except ImportError as e:
    print(f"⚠️ GUI библиотеки недоступны: {e}")
    GUI_AVAILABLE = False

# Дополнительные библиотеки для Windows
try:
    import winreg
    WINDOWS_FEATURES = True
except ImportError:
    WINDOWS_FEATURES = False

class TerminalController:
    """Контроллер терминала"""
    def __init__(self):
        pass
    
    def run(self, command):
        """Выполняет команду в терминале"""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return f"Error: {str(e)}"

class ClipboardController:
    """Контроллер буфера обмена"""
    def __init__(self):
        pass
    
    def copy(self, text):
        """Копирует текст в буфер обмена"""
        pyautogui.copy(text)
    
    def paste(self):
        """Вставляет текст из буфера обмена"""
        return pyautogui.paste()

class DisplayController:
    """Контроллер дисплея"""
    def __init__(self):
        pass
    
    def screenshot(self):
        """Делает скриншот"""
        return pyautogui.screenshot()

class MouseController:
    """Контроллер мыши"""
    def __init__(self):
        pass
    
    def click(self, x, y):
        """Кликает по координатам"""
        pyautogui.click(x, y)
    
    def move(self, x, y):
        """Перемещает мышь"""
        pyautogui.moveTo(x, y)

class KeyboardController:
    """Контроллер клавиатуры"""
    def __init__(self):
        pass
    
    def type(self, text):
        """Печатает текст"""
        pyautogui.typewrite(text)
    
    def press(self, key):
        """Нажимает клавишу"""
        pyautogui.press(key)

class ComputerController:
    """Контроллер для управления компьютером"""
    
    def __init__(self):
        self.screen_size = pyautogui.size()
        # Добавляем атрибуты для совместимости с Open Interpreter
        self.terminal = TerminalController()
        self.clipboard = ClipboardController()
        self.display = DisplayController()
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        
    def find_and_launch_music_app(self):
        """Находит и запускает музыкальное приложение"""
        music_apps = [
            ("Spotify", ["spotify.exe", "Spotify.exe"]),
            ("VLC", ["vlc.exe"]),
            ("Windows Media Player", ["wmplayer.exe"]),
            ("iTunes", ["iTunes.exe"]),
            ("AIMP", ["AIMP.exe"]),
            ("foobar2000", ["foobar2000.exe"]),
        ]
        
        # Сначала проверяем запущенные процессы
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name'].lower()
                if any(app.lower() in proc_name for _, apps in music_apps for app in apps):
                    print(f"🎵 Найдено запущенное музыкальное приложение: {proc.info['name']}")
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Пытаемся запустить приложения
        for app_name, executables in music_apps:
            for exe in executables:
                try:
                    # Ищем в стандартных путях
                    paths_to_check = [
                        f"C:\\Program Files\\{app_name}\\{exe}",
                        f"C:\\Program Files (x86)\\{app_name}\\{exe}",
                        f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\{app_name}\\{exe}",
                        f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Roaming\\{app_name}\\{exe}",
                    ]
                    
                    for path in paths_to_check:
                        if os.path.exists(path):
                            print(f"🎵 Запускаю {app_name}: {path}")
                            subprocess.Popen([path])
                            time.sleep(3)
                            return True
                    
                    # Пытаемся запустить через PATH
                    try:
                        subprocess.Popen([exe])
                        print(f"🎵 Запущен {app_name} через PATH")
                        time.sleep(3)
                        return True
                    except FileNotFoundError:
                        continue
                        
                except Exception as e:
                    continue
        
        # Пытаемся открыть YouTube Music в браузере
        try:
            import webbrowser
            webbrowser.open("https://music.youtube.com")
            print("🎵 Открыт YouTube Music в браузере")
            return True
        except:
            pass
            
        return False
    
    def control_media(self, action):
        """Управление медиа (play/pause/stop/next/previous)"""
        media_keys = {
            'play': 'playpause',
            'pause': 'playpause', 
            'stop': 'stop',
            'next': 'nexttrack',
            'previous': 'prevtrack',
            'volume_up': 'volumeup',
            'volume_down': 'volumedown',
            'mute': 'volumemute'
        }
        
        if action.lower() in media_keys:
            pyautogui.press(media_keys[action.lower()])
            print(f"🎵 Выполнено действие: {action}")
            return True
        return False
    
    def find_application(self, app_name):
        """Находит приложение по имени"""
        print(f"🔍 Ищу приложение: {app_name}")
        
        # Проверяем запущенные процессы
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if app_name.lower() in proc.info['name'].lower():
                    print(f"✅ Найден запущенный процесс: {proc.info['name']}")
                    return proc.info
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Ищем в реестре Windows
        try:
            registry_paths = [
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ]
            
            for reg_path in registry_paths:
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
                        for i in range(winreg.QueryInfoKey(key)[0]):
                            try:
                                subkey_name = winreg.EnumKey(key, i)
                                with winreg.OpenKey(key, subkey_name) as subkey:
                                    try:
                                        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                        if app_name.lower() in display_name.lower():
                                            try:
                                                install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                                print(f"✅ Найдено в реестре: {display_name} -> {install_location}")
                                                return {"name": display_name, "path": install_location}
                                            except FileNotFoundError:
                                                pass
                                    except FileNotFoundError:
                                        pass
                            except OSError:
                                continue
                except OSError:
                    continue
        except Exception as e:
            print(f"⚠️ Ошибка поиска в реестре: {e}")
        
        print(f"❌ Приложение '{app_name}' не найдено")
        return None
    
    def search_files(self, pattern, directory=None):
        """Ищет файлы по паттерну"""
        if directory is None:
            directory = Path.home()
        else:
            directory = Path(directory)
        
        results = []
        try:
            for file in directory.rglob(pattern):
                if file.is_file():
                    results.append(str(file))
                    if len(results) >= 50:  # Ограничиваем количество результатов
                        break
        except PermissionError:
            pass
        except Exception as e:
            print(f"⚠️ Ошибка поиска файлов: {e}")
        
        return results
    
    def take_screenshot(self, filename=None):
        """Делает скриншот экрана"""
        if filename is None:
            filename = f"screenshot_{int(time.time())}.png"
        
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filename)
            print(f"📸 Скриншот сохранен: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Ошибка создания скриншота: {e}")
            return None
    
    def click_image(self, image_path, confidence=0.8):
        """Кликает на изображение на экране"""
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                pyautogui.click(center)
                print(f"🖱️ Клик по изображению: {image_path}")
                return True
            else:
                print(f"❌ Изображение не найдено: {image_path}")
                return False
        except Exception as e:
            print(f"❌ Ошибка поиска изображения: {e}")
            return False
    
    def type_text(self, text):
        """Печатает текст"""
        try:
            pyautogui.typewrite(text, interval=0.05)
            print(f"⌨️ Напечатан текст: {text[:50]}...")
            return True
        except Exception as e:
            print(f"❌ Ошибка ввода текста: {e}")
            return False
    
    def press_keys(self, keys):
        """Нажимает клавиши или комбинацию клавиш"""
        try:
            if isinstance(keys, str):
                pyautogui.press(keys)
            elif isinstance(keys, list):
                pyautogui.hotkey(*keys)
            print(f"⌨️ Нажаты клавиши: {keys}")
            return True
        except Exception as e:
            print(f"❌ Ошибка нажатия клавиш: {e}")
            return False

# Глобальный экземпляр контроллера
computer = ComputerController()

# Функции для совместимости с Open Interpreter
def find_and_launch_music_app():
    """Находит и запускает музыкальное приложение"""
    return computer.find_and_launch_music_app()

def control_media(action):
    """Управление медиа"""
    return computer.control_media(action)

def find_application(app_name):
    """Находит приложение"""
    return computer.find_application(app_name)

def search_files(pattern, directory=None):
    """Ищет файлы"""
    return computer.search_files(pattern, directory)

def take_screenshot(filename=None):
    """Делает скриншот"""
    return computer.take_screenshot(filename)

def click_image(image_path, confidence=0.8):
    """Кликает на изображение"""
    return computer.click_image(image_path, confidence)

def type_text(text):
    """Печатает текст"""
    return computer.type_text(text)

def press_keys(keys):
    """Нажимает клавиши"""
    return computer.press_keys(keys)

# === РАСШИРЕННЫЕ ФУНКЦИИ УПРАВЛЕНИЯ МЕДИА ===

def smart_media_control(action="play"):
    """
    Умное управление медиа - пытается найти и управлять любым медиа приложением
    Actions: play, pause, stop, next, previous, volume_up, volume_down
    """
    if not GUI_AVAILABLE:
        return "❌ GUI библиотеки недоступны"
    
    try:
        print(f"🎵 Выполняю действие с медиа: {action}")
        
        # Сначала пробуем стандартные медиа клавиши
        media_keys = {
            'play': 'playpause',
            'pause': 'playpause', 
            'stop': 'stop',
            'next': 'nexttrack',
            'previous': 'prevtrack',
            'volume_up': 'volumeup',
            'volume_down': 'volumedown'
        }
        
        if action in media_keys:
            print(f"🎹 Нажимаю медиа клавишу: {media_keys[action]}")
            pyautogui.press(media_keys[action])
            time.sleep(0.5)
            return f"✅ Медиа команда '{action}' выполнена"
        
        return f"❌ Неизвестное действие: {action}"
        
    except Exception as e:
        return f"❌ Ошибка управления медиа: {str(e)}"

def find_and_control_spotify():
    """Находит и управляет Spotify"""
    if not GUI_AVAILABLE:
        return "❌ GUI библиотеки недоступны"
    
    try:
        # Ищем окно Spotify
        spotify_found = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'spotify' in proc.info['name'].lower():
                    spotify_found = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if not spotify_found:
            print("🎵 Spotify не найден, пытаюсь запустить...")
            # Пытаемся запустить Spotify
            try:
                subprocess.Popen(['spotify'])
                time.sleep(3)
                return "✅ Spotify запущен"
            except:
                return "❌ Не удалось запустить Spotify"
        
        # Spotify найден, управляем им
        print("🎵 Spotify найден, отправляю команду воспроизведения")
        pyautogui.press('playpause')
        return "✅ Команда отправлена в Spotify"
        
    except Exception as e:
        return f"❌ Ошибка управления Spotify: {str(e)}"

def launch_music_app():
    """Запускает доступное музыкальное приложение"""
    if not GUI_AVAILABLE:
        return "❌ GUI библиотеки недоступны"
    
    music_apps = [
        ("Spotify", ["spotify", "Spotify.exe"]),
        ("VLC", ["vlc", "vlc.exe"]),
        ("Windows Media Player", ["wmplayer", "wmplayer.exe"]),
        ("iTunes", ["iTunes", "iTunes.exe"]),
        ("AIMP", ["aimp", "AIMP.exe"]),
    ]
    
    # Проверяем уже запущенные
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_name = proc.info['name'].lower()
            for app_name, commands in music_apps:
                if any(cmd.lower().replace('.exe', '') in proc_name for cmd in commands):
                    print(f"🎵 {app_name} уже запущен")
                    return f"✅ {app_name} готов к использованию"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Пытаемся запустить
    for app_name, commands in music_apps:
        for cmd in commands:
            try:
                print(f"🎵 Пытаюсь запустить {app_name}...")
                subprocess.Popen([cmd], shell=True)
                time.sleep(2)
                return f"✅ {app_name} запущен"
            except Exception as e:
                continue
    
    return "❌ Не удалось найти или запустить музыкальное приложение"

def advanced_click_by_image(image_name, confidence=0.8, timeout=5):
    """
    Продвинутый поиск и клик по изображению
    """
    if not GUI_AVAILABLE:
        return "❌ GUI библиотеки недоступны"
    
    try:
        # Создаем папку для изображений если её нет
        current_dir = Path(__file__).parent if __file__ else Path.cwd()
        images_dir = current_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        # Делаем скриншот
        screenshot = pyautogui.screenshot()
        
        # Пытаемся найти изображение
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(image_name, confidence=confidence)
                if location:
                    center = pyautogui.center(location)
                    pyautogui.click(center)
                    return f"✅ Кликнул по изображению {image_name} в позиции {center}"
            except pyautogui.ImageNotFoundException:
                pass
            time.sleep(0.5)
        
        return f"❌ Изображение {image_name} не найдено на экране"
        
    except Exception as e:
        return f"❌ Ошибка поиска изображения: {str(e)}"

def smart_window_control(app_name, action="activate"):
    """
    Умное управление окнами приложений
    Actions: activate, minimize, maximize, close
    """
    if not GUI_AVAILABLE:
        return "❌ GUI библиотеки недоступны"
    
    try:
        import pygetwindow as gw
        
        # Ищем окна с указанным именем
        windows = gw.getWindowsWithTitle(app_name)
        if not windows:
            # Ищем по частичному совпадению
            all_windows = gw.getAllWindows()
            windows = [w for w in all_windows if app_name.lower() in w.title.lower()]
        
        if not windows:
            return f"❌ Окно с именем '{app_name}' не найдено"
        
        window = windows[0]  # Берем первое найденное окно
        
        if action == "activate":
            window.activate()
            return f"✅ Окно '{window.title}' активировано"
        elif action == "minimize":
            window.minimize()
            return f"✅ Окно '{window.title}' минимизировано"
        elif action == "maximize":
            window.maximize()
            return f"✅ Окно '{window.title}' максимизировано"
        elif action == "close":
            window.close()
            return f"✅ Окно '{window.title}' закрыто"
        else:
            return f"❌ Неизвестное действие: {action}"
            
    except Exception as e:
        return f"❌ Ошибка управления окном: {str(e)}"
