#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_connection():
    try:
        print("🔗 Попытка подключения к ws://localhost:8765...")
        async with websockets.connect('ws://localhost:8765') as websocket:
            print('✅ Подключение к WebSocket успешно!')
            
            # Отправляем тестовое сообщение
            test_message = {'message': 'привет'}
            await websocket.send(json.dumps(test_message))
            print('📤 Сообщение отправлено:', test_message)
            
            # Ждем ответ
            response = await websocket.recv()
            print(f'📥 Получен ответ: {response}')
            
    except Exception as e:
        print(f'❌ Ошибка подключения: {e}')

if __name__ == "__main__":
    asyncio.run(test_connection())
