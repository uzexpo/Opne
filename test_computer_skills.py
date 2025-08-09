#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест новых компьютерных возможностей Open Interpreter
"""

import asyncio
import websockets
import json
import time

async def test_music_capabilities():
    """Тестирует музыкальные возможности"""
    uri = "ws://localhost:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🧪 Тестирование музыкальных возможностей...")
            
            # Тест 1: Включение музыки
            test_message = {
                "message": "Включи музыку"
            }
            
            print(f"📤 Отправляем: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Ожидаем ответы
            response_count = 0
            max_responses = 10
            
            while response_count < max_responses:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=30.0)
                    data = json.loads(response)
                    print(f"📥 Получен ответ: {data}")
                    
                    if data.get('type') == 'response':
                        print("✅ Тест включения музыки завершен!")
                        break
                        
                    response_count += 1
                    
                except asyncio.TimeoutError:
                    print("⏰ Timeout - завершаем тест")
                    break
            
            # Небольшая пауза
            await asyncio.sleep(2)
            
            # Тест 2: Управление воспроизведением
            control_message = {
                "message": "Поставь музыку на паузу"
            }
            
            print(f"📤 Отправляем: {control_message}")
            await websocket.send(json.dumps(control_message))
            
            # Ожидаем ответ
            response_count = 0
            while response_count < max_responses:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                    data = json.loads(response)
                    print(f"📥 Получен ответ: {data}")
                    
                    if data.get('type') == 'response':
                        print("✅ Тест управления музыкой завершен!")
                        break
                        
                    response_count += 1
                    
                except asyncio.TimeoutError:
                    print("⏰ Timeout - завершаем тест")
                    break
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

async def test_app_search():
    """Тестирует поиск приложений"""
    uri = "ws://localhost:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🧪 Тестирование поиска приложений...")
            
            test_message = {
                "message": "Найди и открой калькулятор"
            }
            
            print(f"📤 Отправляем: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Ожидаем ответы
            response_count = 0
            max_responses = 8
            
            while response_count < max_responses:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=20.0)
                    data = json.loads(response)
                    print(f"📥 Получен ответ: {data}")
                    
                    if data.get('type') == 'response':
                        print("✅ Тест поиска приложений завершен!")
                        break
                        
                    response_count += 1
                    
                except asyncio.TimeoutError:
                    print("⏰ Timeout - завершаем тест")
                    break
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")

async def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов компьютерных возможностей Open Interpreter...")
    print("=" * 60)
    
    # Тест 1: Музыкальные возможности
    await test_music_capabilities()
    
    print("\n" + "=" * 60)
    
    # Тест 2: Поиск и запуск приложений
    await test_app_search()
    
    print("\n" + "=" * 60)
    print("🎉 Все тесты завершены!")

if __name__ == "__main__":
    asyncio.run(main())
