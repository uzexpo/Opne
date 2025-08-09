#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простой тест музыкальных возможностей
"""

import asyncio
import websockets
import json

async def simple_music_test():
    """Простой тест включения музыки"""
    uri = "ws://localhost:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🧪 Простой тест включения музыки...")
            
            # Простая команда
            test_message = {
                "message": "Включи музыку используя play_music()"
            }
            
            print(f"📤 Отправляем: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Ожидаем ответы
            for i in range(15):  # Ждем максимум 15 ответов
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=10.0)
                    data = json.loads(response)
                    print(f"📥 [{i+1}] {data}")
                    
                    if data.get('type') == 'response':
                        print("✅ Команда выполнена!")
                        return
                        
                except asyncio.TimeoutError:
                    print("⏰ Timeout")
                    break
                except Exception as e:
                    print(f"❌ Ошибка: {e}")
                    break
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    asyncio.run(simple_music_test())
