import asyncio, json, websockets, os

PORT = int(os.getenv("OI_WS_PORT", "8765"))
WS_URL = f"ws://localhost:{PORT}"

async def send(msg):
    async with websockets.connect(WS_URL) as ws:
        await ws.send(json.dumps(msg))
        reply = await ws.recv()
        print("REPLY:", reply)

async def main():
    # старт сервиса браузера
    await send({"type":"tool_call","tool":"browser.service.start","args":{"port":8787}})
    await send({"type":"tool_call","tool":"browser.service.health","args":{}})
    # аудио очередь и проигрывание
    await send({"type":"tool_call","tool":"audio.queue","args":{"items":["https://samplelib.com/lib/preview/mp3/sample-3s.mp3"]}})
    await send({"type":"tool_call","tool":"audio.next","args":{"volume":70}})
    # браузер: открыть + play_audio + скриншот
    await send({"type":"tool_call","tool":"browser.open","args":{"url":"https://example.com","auto_play":False,"duration":2}})
    await send({"type":"tool_call","tool":"browser.playAudio","args":{"page_url":"https://example.com","audio_url":"https://samplelib.com/lib/preview/mp3/sample-3s.mp3","duration":3}})
    await send({"type":"tool_call","tool":"browser.screenshot","args":{"path":"logs/smoke.png"}})
    # стоп сервиса
    await send({"type":"tool_call","tool":"browser.service.stop","args":{}})

if __name__ == "__main__":
    asyncio.run(main())
