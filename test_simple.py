#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тест сервера без сложных команд
"""

import asyncio
import websockets
import json

async def test_simple():
    """Простой тест основных функций"""
    uri = "ws://192.168.241.1:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🧪 Простой тест...")
            print(f"🔗 Подключение к: {uri}")
            
            # Простая команда без файлов
            test_message = {
                "message": "Скажи привет и покажи текущее время"
            }
            
            print(f"📤 Отправляем: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Ожидаем ответы
            for i in range(10):
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
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
    asyncio.run(test_simple())
