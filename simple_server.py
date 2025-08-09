#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import asyncio
import websockets
from dotenv import load_dotenv
import logging
import subprocess
import time

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleInterpreterServer:
    def __init__(self):
        self.clients = set()
        
    async def register(self, websocket):
        self.clients.add(websocket)
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
        
    async def unregister(self, websocket):
        self.clients.remove(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
        
    async def send_to_client(self, websocket, message):
        try:
            await websocket.send(json.dumps(message))
        except websockets.exceptions.ConnectionClosed:
            pass
    
    async def execute_simple_command(self, command):
        """Выполняет простые команды без Open Interpreter"""
        
        if "привет" in command.lower():
            return "👋 Привет! Я готов помочь вам с компьютером!"
        
        if "время" in command.lower():
            import datetime
            current_time = datetime.datetime.now().strftime('%H:%M:%S %d.%m.%Y')
            return f"🕐 Текущее время: {current_time}"
            
        if "калькулятор" in command.lower():
            try:
                subprocess.Popen(['calc.exe'])
                return "✅ Калькулятор запущен!"
            except Exception as e:
                return f"❌ Ошибка запуска калькулятора: {e}"
        
        if "блокнот" in command.lower():
            try:
                subprocess.Popen(['notepad.exe'])
                return "✅ Блокнот запущен!"
            except Exception as e:
                return f"❌ Ошибка запуска блокнота: {e}"
                
        if "проводник" in command.lower():
            try:
                subprocess.Popen(['explorer.exe'])
                return "✅ Проводник запущен!"
            except Exception as e:
                return f"❌ Ошибка запуска проводника: {e}"
        
        if "браузер" in command.lower() or "интернет" in command.lower():
            try:
                subprocess.Popen(['start', 'https://www.google.com'], shell=True)
                return "✅ Браузер запущен!"
            except Exception as e:
                return f"❌ Ошибка запуска браузера: {e}"
        
        return f"🤖 Получил команду: '{command}'. Базовые команды: привет, время, калькулятор, блокнот, проводник, браузер"
    
    async def handle_message(self, websocket):
        await self.register(websocket)
        try:
            # Отправляем приветствие
            await self.send_to_client(websocket, {
                "type": "system",
                "message": "🤖 Simple Interpreter готов к работе!"
            })
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    user_message = data.get('message', '')
                    
                    if user_message.strip():
                        # Отправляем подтверждение получения
                        await self.send_to_client(websocket, {
                            "type": "user_echo",
                            "message": user_message
                        })
                        
                        # Отправляем статус обработки
                        await self.send_to_client(websocket, {
                            "type": "processing",
                            "message": "🔄 Обрабатываю запрос..."
                        })
                        
                        try:
                            # Выполняем простую команду
                            response = await self.execute_simple_command(user_message)
                            
                            # Отправляем результат
                            await self.send_to_client(websocket, {
                                "type": "response",
                                "message": response
                            })
                            
                        except Exception as e:
                            error_msg = f"❌ Ошибка выполнения: {str(e)}"
                            logger.error(error_msg)
                            await self.send_to_client(websocket, {
                                "type": "error",
                                "message": error_msg
                            })
                            
                except json.JSONDecodeError:
                    await self.send_to_client(websocket, {
                        "type": "error",
                        "message": "❌ Ошибка формата сообщения"
                    })
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

def main():
    print("🚀 Запуск Simple Interpreter сервера...")
    print("📡 WebSocket сервер будет доступен на ws://192.168.241.1:8765")
    print("📡 Также доступен локально на ws://localhost:8765")
    
    server = SimpleInterpreterServer()
    
    async def run_server():
        start_server = websockets.serve(
            server.handle_message, 
            "0.0.0.0",
            8765,
            ping_interval=20,
            ping_timeout=20
        )
        
        await start_server
        print("✅ Сервер запущен успешно!")
        await asyncio.Future()  # run forever
    
    asyncio.run(run_server())

if __name__ == "__main__":
    main()
