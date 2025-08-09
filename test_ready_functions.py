#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрый тест готовых функций
"""

import asyncio
import websockets
import json

async def test_ready_functions():
    """Тестирует готовые функции музыки"""
    uri = "ws://192.168.241.1:8765"  # Используем IP-адрес компьютера
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🧪 Тест готовых функций...")
            print(f"🔗 Подключение к: {uri}")
            
            # Простая команда с использованием системных функций
            test_message = {
                "message": "Открой калькулятор Windows"
            }
            
            print(f"📤 Отправляем: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Ожидаем ответы
            for i in range(10):
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(response)
                    print(f"📥 [{i+1}] {data}")
                    
                    if data.get('type') == 'response':
                        print("✅ Функция выполнена!")
                        break
                        
                except asyncio.TimeoutError:
                    print("⏰ Timeout")
                    break
                except Exception as e:
                    print(f"❌ Ошибка: {e}")
                    break
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    asyncio.run(test_ready_functions())
