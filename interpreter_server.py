#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os
from interpreter import interpreter

# Настройка кодировки для Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# Настройка Open Interpreter
interpreter.auto_run = True
interpreter.local = True
interpreter.model = "openai/gpt-4o-mini"

# Установка API ключа
api_key = os.environ.get('OPENAI_API_KEY')
if api_key:
    interpreter.api_key = api_key

def send_response(response_type, data):
    """Отправляет ответ в JSON формате"""
    response = {
        'type': response_type,
        'data': data
    }
    print(json.dumps(response, ensure_ascii=False))
    sys.stdout.flush()

def main():
    send_response('ready', 'Open Interpreter готов к работе!')
    
    try:
        while True:
            line = input()
            if not line.strip():
                continue
                
            if line.strip().lower() in ['exit', 'quit', 'выход']:
                send_response('exit', 'До свидания!')
                break
            
            try:
                # Выполняем команду через Open Interpreter
                send_response('thinking', 'Обрабатываю команду...')
                
                result = interpreter.chat(line)
                
                # Извлекаем текстовый ответ
                response_text = ""
                for chunk in result:
                    if hasattr(chunk, 'content') and chunk.content:
                        response_text += chunk.content
                    elif isinstance(chunk, dict) and 'content' in chunk:
                        response_text += chunk['content']
                    elif isinstance(chunk, str):
                        response_text += chunk
                
                if response_text.strip():
                    send_response('response', response_text.strip())
                else:
                    send_response('response', 'Команда выполнена.')
                    
            except Exception as e:
                send_response('error', f'Ошибка: {str(e)}')
                
    except KeyboardInterrupt:
        send_response('exit', 'Завершение работы...')
    except EOFError:
        send_response('exit', 'Соединение закрыто.')

if __name__ == '__main__':
    main()
