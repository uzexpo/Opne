#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест запуска калькулятора
"""

import asyncio
import websockets
import json

async def test_calc():
    uri = "ws://192.168.241.1:8765"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("🧮 Тест калькулятора...")
            
            test_message = {
                "message": "Открой калькулятор"
            }
            
            print(f"📤 Отправляем: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            for i in range(5):
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(response)
                    print(f"📥 [{i+1}] {data}")
                    
                    if data.get('type') == 'response':
                        print("✅ Калькулятор команда выполнена!")
                        break
                        
                except asyncio.TimeoutError:
                    print("⏰ Timeout")
                    break
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(test_calc())
