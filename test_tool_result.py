#!/usr/bin/env python3
"""Тест tool_call для проверки возврата stdout/stderr"""

import asyncio
import websockets
import json

async def test_tool_call():
    uri = "ws://localhost:8765"
    print(f"🔗 Подключение к {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Подключено к WebSocket серверу")
            
            # Тест 1: audio.play
            test_payload = {
                "tool": "audio.play",
                "args": {
                    "source": "https://samplelib.com/lib/preview/mp3/sample-3s.mp3",
                    "volume": 70
                }
            }
            
            print("🧪 Отправляем tool_call:", json.dumps(test_payload, indent=2))
            await websocket.send(json.dumps(test_payload))
            
            response = await websocket.recv()
            result = json.loads(response)
            
            print("📩 Получен ответ:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # Проверяем структуру ответа
            expected_fields = ["ok", "rc", "out", "err", "cmd"]
            if all(field in result for field in expected_fields):
                print("✅ Все ожидаемые поля присутствуют!")
            else:
                print("❌ Не хватает полей:", [f for f in expected_fields if f not in result])
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(test_tool_call())
