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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--open", help="Открыть URL")
    ap.add_argument("--play-audio-url", help="Проиграть аудио URL в странице через <audio>")
    ap.add_argument("--click", help="CSS селектор для клика")
    ap.add_argument("--duration", type=int, default=10, help="Держать окно N сек")
    ap.add_argument("--channel", default="msedge", choices=["msedge","chrome","chromium"])
    ap.add_argument("--auto-play", action="store_true", help="Автоматически искать и кликать кнопку воспроизведения")
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
            if try_autoplay_click(page):
                print("OK: auto-play click succeeded")

        if args.play_audio_url:
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

        time.sleep(max(1, args.duration))
        browser.close()
        print("OK: browser task done")

if __name__ == "__main__":
    main()
