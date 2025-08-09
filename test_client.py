#!/usr/bin/env python3
"""
Простой тест клиент для проверки WebSocket соединения
"""

import asyncio
import websockets
import json
import sys

async def test_connection():
    uri = "ws://localhost:8765"
    
    try:
        print("🔌 Подключение к серверу...")
        async with websockets.connect(uri) as websocket:
            print("✅ Соединение установлено!")
            
            # Отправляем тестовое сообщение
            test_message = {
                "message": "Привет! Это тест соединения."
            }
            
            print(f"📤 Отправляем: {test_message}")
            await websocket.send(json.dumps(test_message))
            
            # Ждем ответ
            print("⏳ Ожидание ответа...")
            
            timeout_count = 0
            max_timeout = 30  # 30 секунд
            
            while timeout_count < max_timeout:
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(response)
                    print(f"📥 Получен ответ: {data}")
                    
                    if data.get('type') == 'response':
                        print("✅ Тест завершен успешно!")
                        return True
                        
                except asyncio.TimeoutError:
                    timeout_count += 1
                    print(f"⏳ Ожидание... ({timeout_count}/{max_timeout})")
                    continue
                    
            print("⚠️ Таймаут ожидания ответа")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Запуск теста WebSocket соединения...")
    success = asyncio.run(test_connection())
    
    if success:
        print("🎉 Тест прошел успешно!")
        sys.exit(0)
    else:
        print("💥 Тест не прошел!")
        sys.exit(1)
