#!/usr/bin/env python3
import asyncio
import websockets
import json

async def test_tool_calls():
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Подключен к серверу")
            
            # Тест 1: audio.play
            print("\n🎵 Тест 1: audio.play")
            message1 = {
                "type": "tool_call",
                "tool": "audio.play",
                "args": {
                    "source": "https://samplelib.com/lib/preview/mp3/sample-3s.mp3",
                    "volume": 85
                }
            }
            await websocket.send(json.dumps(message1))
            response1 = await websocket.recv()
            print(f"Ответ: {response1}")
            
            await asyncio.sleep(4)  # Ждем окончания воспроизведения
            
            # Тест 2: browser.playAudio
            print("\n🌐 Тест 2: browser.playAudio")
            message2 = {
                "type": "tool_call",
                "tool": "browser.playAudio",
                "args": {
                    "page_url": "https://example.com",
                    "audio_url": "https://samplelib.com/lib/preview/mp3/sample-3s.mp3",
                    "duration": 6
                }
            }
            await websocket.send(json.dumps(message2))
            response2 = await websocket.recv()
            print(f"Ответ: {response2}")
            
            await asyncio.sleep(7)  # Ждем окончания браузера
            
            # Тест 3: audio.stop
            print("\n🛑 Тест 3: audio.stop")
            message3 = {
                "type": "tool_call",
                "tool": "audio.stop",
                "args": {}
            }
            await websocket.send(json.dumps(message3))
            response3 = await websocket.recv()
            print(f"Ответ: {response3}")
            
            print("\n✅ Все тесты завершены!")
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(test_tool_calls())
