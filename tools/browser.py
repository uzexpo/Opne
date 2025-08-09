import argparse, time
from playwright.sync_api import sync_playwright

# Популярные селекторы кнопок воспроизведения
PLAY_SELECTORS = [
    "button[aria-label*='Play']",
    "button[aria-label*='Воспроизвести']", 
    "button[aria-label*='play']",
    ".ytp-play-button",
    ".ytp-large-play-button", 
    "button[data-purpose='play-button']",
    ".play-button",
    ".play-btn",
    "[data-testid='play-button']",
    "button[title*='Play']",
    "button[title*='Воспроизвести']"
]

def try_autoplay_click(page):
    """Попытка автоматического клика по кнопке воспроизведения"""
    for selector in PLAY_SELECTORS:
        try:
            element = page.query_selector(selector)
            if element and element.is_visible():
                element.click()
                print(f"OK: clicked {selector}")
                return True
        except Exception as e:
            continue
    return False

def try_start_audio(page):
    """Улучшенная функция запуска аудио с множественными стратегиями"""
    selectors = [
        ".ytp-play-button", "button.ytp-large-play-button", "button[aria-label^='Play']",
        "button[aria-label='Play (k)']",
        "button[title='Play (k)']",
        "video"
    ]
    for sel in selectors:
        try:
            if sel == "video":
                page.evaluate("document.querySelector('video')?.play()?.catch(()=>{})")
                print(f"OK: tried video.play() via evaluate")
                return True
            else:
                page.click(sel, timeout=1500)
                print(f"OK: clicked {sel}")
                return True
        except Exception:
            pass
    # на всякий случай пробуем клавишу 'k' (YouTube hotkey)
    try:
        page.keyboard.press("k")
        print("OK: pressed 'k' hotkey")
        return True
    except Exception:
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--open", help="Открыть URL")
    ap.add_argument("--play-audio-url", help="Проиграть аудио URL в странице через <audio>")
    ap.add_argument("--click", help="CSS селектор для клика")
    ap.add_argument("--duration", type=int, default=10, help="Держать окно N сек")
    ap.add_argument("--channel", default="msedge", choices=["msedge","chrome","chromium"])
    ap.add_argument("--auto-play", action="store_true", help="Автоматически искать и кликать кнопку воспроизведения")
    ap.add_argument("--screenshot", help="Путь для сохранения скриншота")
    args = ap.parse_args()

    with sync_playwright() as p:
        if args.channel == "msedge":
            browser = p.chromium.launch(channel="msedge", headless=False, args=[
                "--autoplay-policy=no-user-gesture-required",
                "--disable-features=VizDisplayCompositor"
            ])
        elif args.channel == "chrome":
            browser = p.chromium.launch(channel="chrome", headless=False, args=[
                "--autoplay-policy=no-user-gesture-required",
                "--disable-features=VizDisplayCompositor"
            ])
        else:
            browser = p.chromium.launch(headless=False, args=[
                "--autoplay-policy=no-user-gesture-required",
                "--disable-features=VizDisplayCompositor"
            ])

        ctx = browser.new_context()
        page = ctx.new_page()

        # Обработка скриншота
        if args.screenshot:
            # Если нужен только скриншот без открытия URL
            if not args.open:
                page.goto("about:blank")
            page.screenshot(path=args.screenshot)
            print(f"OK: screenshot saved to {args.screenshot}")
            if not args.open:  # Если только скриншот, завершаем
                browser.close()
                return

        if args.open:
            page.goto(args.open, wait_until="domcontentloaded")
            time.sleep(2)  # Даем время для загрузки

        if args.click:
            try:
                page.click(args.click, timeout=5000)
                print(f"OK: clicked {args.click}")
            except Exception as e:
                print(f"WARN CLICK: {e}")
                # Если указанный селектор не сработал, пробуем автоплей
                if args.open and ("youtube" in args.open.lower() or "music" in args.open.lower()):
                    if try_autoplay_click(page):
                        print("OK: fallback autoplay click succeeded")

        if args.auto_play and args.open:
            time.sleep(1)
            if try_start_audio(page):
                print("OK: auto-play with try_start_audio succeeded")
            elif try_autoplay_click(page):
                print("OK: auto-play fallback with try_autoplay_click succeeded")

        if args.play_audio_url:
            # Оставляем текущий <audio>-подход для внешних URL
            page.evaluate("""
                url => {
                  const a = new Audio(url);
                  a.autoplay = true;
                  a.loop = false;
                  a.volume = 1.0;
                  a.crossOrigin = "anonymous";
                  document.body.appendChild(a);
                  a.play().then(() => console.log('Audio started')).catch(e => console.error('Audio failed:', e));
                }
            """, args.play_audio_url)
        elif args.open and not args.click:
            # Если нет --play-audio-url, пробуем try_start_audio для видео на странице
            time.sleep(1)
            if try_start_audio(page):
                print("OK: page video auto-start succeeded")

        # Делаем скриншот в конце, если указан путь
        if args.screenshot and args.open:
            page.screenshot(path=args.screenshot)
            print(f"OK: final screenshot saved to {args.screenshot}")

        time.sleep(max(1, args.duration))
        browser.close()
        print("OK: browser task done")

if __name__ == "__main__":
    main()
