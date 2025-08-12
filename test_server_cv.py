#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 ПРЯМОЙ ТЕСТ SIMPLE CV НА СЕРВЕРЕ 🧪
Тестируем новые простые функции прямо на запущенном сервере
"""

import asyncio
import websockets
import json
import time

async def test_play_button():
    """Тест поиска и клика по кнопке Play через WebSocket"""
    
    uri = "ws://localhost:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🔗 Подключение к серверу Open Interpreter...")
            
            # Ждем приветствие
            greeting = await websocket.recv()
            print(f"📩 Приветствие: {json.loads(greeting)}")
            
            # Тест 1: Простой тест поиска кнопки Play
            print("\n🧪 Тест 1: Поиск кнопки Play...")
            test_message = {
                "message": "найди кнопку play на экране"
            }
            
            await websocket.send(json.dumps(test_message))
            
            # Читаем ответы
            for i in range(5):  # Максимум 5 ответов
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    data = json.loads(response)
                    print(f"📥 Ответ {i+1}: {data.get('type', 'unknown')} - {data.get('message', '')[:100]}...")
                    
                    if data.get('type') == 'response':
                        break
                except asyncio.TimeoutError:
                    print("⏰ Таймаут ожидания ответа")
                    break
            
            print("\n" + "="*50)
            
            # Тест 2: Клик по кнопке Play
            print("\n🧪 Тест 2: Клик по кнопке Play...")
            click_message = {
                "message": "кликни по кнопке play чтобы включить музыку"
            }
            
            await websocket.send(json.dumps(click_message))
            
            # Читаем ответы
            for i in range(5):  # Максимум 5 ответов
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=15.0)
                    data = json.loads(response)
                    print(f"📥 Ответ {i+1}: {data.get('type', 'unknown')} - {data.get('message', '')[:100]}...")
                    
                    if data.get('type') == 'response':
                        break
                except asyncio.TimeoutError:
                    print("⏰ Таймаут ожидания ответа")
                    break
            
            print("\n🏁 Тестирование завершено!")
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    print("🚀 Запуск теста простых CV функций...")
    asyncio.run(test_play_button())
