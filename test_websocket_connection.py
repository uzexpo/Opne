#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_connection():
    try:
        print("🔗 Подключаюсь к ws://localhost:8765...")
        
        async with websockets.connect("ws://localhost:8765") as websocket:
            print("✅ Подключение успешно!")
            
            # Отправляем тестовое сообщение
            test_message = {
                "message": "Привет, это тест подключения!"
            }
            
            print("📤 Отправляю тестовое сообщение...")
            await websocket.send(json.dumps(test_message))
            
            # Ждем ответы
            async for message in websocket:
                print(f"📥 Получен ответ: {message}")
                data = json.loads(message)
                if data.get('type') == 'response':
                    print("✅ Тест завершен успешно!")
                    break
                    
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
