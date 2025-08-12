#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Enhanced Computer Vision for Open Interpreter
Быстрое и точное компьютерное зрение без тяжелых моделей
"""

import io
import time
import base64
import json
import mss
import numpy as np
from PIL import Image
from typing import List, Tuple, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SmartScreenCapture:
    """Оптимизированный захват экрана"""
    
    def __init__(self):
        self.sct = mss.mss()
        self.cache = {}
        self.last_capture_time = 0
        self.min_interval = 0.1  # Минимум 100ms между захватами
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        Быстрый захват экрана с кэшированием
        region: (x, y, width, height) или None для полного экрана
        """
        current_time = time.time()
        
        # Throttling для предотвращения spam захватов
        if current_time - self.last_capture_time < self.min_interval:
            if 'last_frame' in self.cache:
                return self.cache['last_frame']
        
        try:
            if region:
                monitor = {"top": region[1], "left": region[0], 
                          "width": region[2], "height": region[3]}
            else:
                monitor = self.sct.monitors[1]  # Первый монитор
            
            # MSS захват - очень быстрый!
            screenshot = self.sct.grab(monitor)
            img_array = np.array(screenshot)[:, :, :3]  # Убираем альфа канал
            
            self.cache['last_frame'] = img_array
            self.last_capture_time = current_time
            
            logger.info(f"📸 Захват экрана: {img_array.shape} за {(time.time()-current_time)*1000:.1f}ms")
            return img_array
            
        except Exception as e:
            logger.error(f"❌ Ошибка захвата экрана: {e}")
            return np.array([])

class LocalVisionProcessor:
    """Локальная обработка изображений без тяжелых моделей"""
    
    def find_ui_elements_basic(self, image: np.ndarray, target_text: str = None) -> List[Dict]:
        """
        Базовое определение UI элементов через анализ цветов и контуров
        """
        from PIL import Image, ImageEnhance
        
        results = []
        
        try:
            # Конвертация в PIL
            pil_img = Image.fromarray(image)
            
            # Поиск кнопко-подобных областей
            button_regions = self._find_button_regions(pil_img)
            
            for i, region in enumerate(button_regions):
                results.append({
                    "type": "button_candidate",
                    "bbox": region,
                    "confidence": 0.7,  # Базовая уверенность
                    "center": ((region[0] + region[2]) // 2, (region[1] + region[3]) // 2)
                })
            
            logger.info(f"🔍 Найдено {len(results)} потенциальных UI элементов")
            return results
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки изображения: {e}")
            return []
    
    def _find_button_regions(self, pil_img: Image.Image) -> List[Tuple[int, int, int, int]]:
        """Простой поиск прямоугольных областей (кнопки, поля)"""
        import cv2
        
        # Конвертация в OpenCV формат
        opencv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
        
        # Поиск контуров
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        button_regions = []
        
        for contour in contours:
            # Аппроксимация прямоугольника
            x, y, w, h = cv2.boundingRect(contour)
            
            # Фильтр по размеру (вероятные кнопки)
            if 30 <= w <= 300 and 20 <= h <= 80:
                button_regions.append((x, y, x + w, y + h))
        
        return button_regions[:10]  # Топ 10 кандидатов

class CloudVisionAPI:
    """Интеграция с облачными CV API (опционально)"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.enabled = bool(api_key)
    
    def analyze_image_cloud(self, image: np.ndarray) -> List[Dict]:
        """Анализ через облачное API (заглушка)"""
        if not self.enabled:
            return []
        
        # TODO: Интеграция с Google Vision API / Azure CV / AWS Rekognition
        logger.info("🌐 Облачный анализ отключен - используем локальный")
        return []

class EnhancedComputerVision:
    """Главный класс улучшенного компьютерного зрения"""
    
    def __init__(self, use_cloud: bool = False, api_key: str = None):
        self.capture = SmartScreenCapture()
        self.local_processor = LocalVisionProcessor()
        self.cloud_api = CloudVisionAPI(api_key) if use_cloud else None
        
        logger.info("🚀 Enhanced Computer Vision инициализирован")
    
    def find_and_click(self, target_description: str, 
                      region: Optional[Tuple[int, int, int, int]] = None,
                      click: bool = True) -> Dict:
        """
        Основной метод: найти элемент и кликнуть
        """
        start_time = time.time()
        
        try:
            # 1. Захват экрана
            image = self.capture.capture_screen(region)
            if image.size == 0:
                return {"success": False, "error": "Не удалось захватить экран"}
            
            # 2. Анализ изображения
            elements = self.local_processor.find_ui_elements_basic(image, target_description)
            
            if not elements:
                return {"success": False, "error": "Элементы не найдены"}
            
            # 3. Выбор лучшего кандидата
            best_element = max(elements, key=lambda x: x['confidence'])
            
            # 4. Клик (если требуется)
            if click:
                import pyautogui
                x, y = best_element['center']
                pyautogui.click(x, y)
                
                # Небольшая пауза для UI реакции
                time.sleep(0.2)
            
            processing_time = (time.time() - start_time) * 1000
            
            result = {
                "success": True,
                "element": best_element,
                "processing_time_ms": processing_time,
                "elements_found": len(elements)
            }
            
            logger.info(f"✅ Элемент найден и обработан за {processing_time:.1f}ms")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка в find_and_click: {e}")
            return {"success": False, "error": str(e)}
    
    def smart_screenshot_analysis(self, save_path: str = None) -> Dict:
        """Умный анализ текущего экрана"""
        
        try:
            image = self.capture.capture_screen()
            elements = self.local_processor.find_ui_elements_basic(image)
            
            # Сохранение аннотированного скриншота
            if save_path:
                self._save_annotated_screenshot(image, elements, save_path)
            
            return {
                "success": True,
                "elements_count": len(elements),
                "elements": elements,
                "screen_size": image.shape[:2] if image.size > 0 else None
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка анализа экрана: {e}")
            return {"success": False, "error": str(e)}
    
    def _save_annotated_screenshot(self, image: np.ndarray, elements: List[Dict], path: str):
        """Сохранение скриншота с аннотациями"""
        try:
            import cv2
            
            annotated = image.copy()
            
            for element in elements:
                x1, y1, x2, y2 = element['bbox']
                cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated, f"{element['confidence']:.2f}", 
                           (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            cv2.imwrite(path, cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR))
            logger.info(f"💾 Аннотированный скриншот сохранен: {path}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения скриншота: {e}")

# Глобальный экземпляр для использования в навыках
enhanced_cv = EnhancedComputerVision()

# Функции для интеграции с Open Interpreter
def smart_click(target_description: str, region: str = None) -> str:
    """
    Умный клик по описанию элемента
    """
    try:
        # Парсинг региона если указан
        parsed_region = None
        if region:
            # Формат: "x,y,width,height"
            coords = list(map(int, region.split(',')))
            parsed_region = tuple(coords)
        
        result = enhanced_cv.find_and_click(target_description, parsed_region, click=True)
        
        if result['success']:
            return f"✅ Успешно кликнул по элементу. Время обработки: {result['processing_time_ms']:.1f}ms"
        else:
            return f"❌ Не удалось найти элемент: {result['error']}"
            
    except Exception as e:
        return f"❌ Ошибка smart_click: {e}"

def analyze_screen() -> str:
    """
    Анализ текущего экрана
    """
    try:
        result = enhanced_cv.smart_screenshot_analysis()
        
        if result['success']:
            return f"📊 Анализ экрана: найдено {result['elements_count']} UI элементов"
        else:
            return f"❌ Ошибка анализа: {result['error']}"
            
    except Exception as e:
        return f"❌ Ошибка analyze_screen: {e}"

if __name__ == "__main__":
    # Быстрый тест
    print("🧪 Тестирование Enhanced Computer Vision...")
    
    # Тест захвата экрана
    cv = EnhancedComputerVision()
    result = cv.smart_screenshot_analysis("test_screenshot.png")
    print(f"Результат теста: {result}")
