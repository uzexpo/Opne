#!/usr/bin/env python3
"""Демонстрация команды для YouTube автоплея"""

print("🎬 STEP D DONE - YouTube/плееры: устойчивый автоплей")
print("\n📋 Добавленные функции:")
print("✅ try_start_audio() - улучшенная функция запуска аудио")
print("✅ Поддержка --auto-play флага")
print("✅ Проверка allowlist доменов")

print("\n🚀 Пример команды для YouTube с автоплеем:")
example_cmd = """
python tools/browser.py --open "https://youtube.com/watch?v=dQw4w9WgXcQ" --auto-play --duration 10
"""
print(example_cmd.strip())

print("\n🔧 Через tool_call:")
example_tool_call = {
    "tool": "browser.open",
    "args": {
        "url": "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "auto_play": True,
        "duration": 10
    }
}
print(f"{example_tool_call}")

print("\n📝 Функция try_start_audio пробует:")
strategies = [
    "1. .ytp-play-button (основная кнопка YouTube)",
    "2. button.ytp-large-play-button (большая кнопка)",
    "3. button[aria-label^='Play'] (доступность)",
    "4. video.play() через JavaScript",
    "5. Клавиша 'k' (YouTube hotkey)"
]

for strategy in strategies:
    print(f"   {strategy}")

print("\n✅ STEP D завершен - устойчивый автоплей для YouTube и других плееров реализован!")
