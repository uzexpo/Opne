import os, time, asyncio
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from playwright.async_api import async_playwright
import threading

APP_HOST = "127.0.0.1"
APP_PORT = int(os.getenv("BROWSERD_PORT", "8787"))

app = FastAPI(title="browserd", version="1.0")

class OpenReq(BaseModel):
    url: str
    new_tab: bool = False
    duration: int = 0
    auto_play: bool = False

class PlayAudioReq(BaseModel):
    page_url: Optional[str] = None
    audio_url: str
    duration: int = 5

class ClickReq(BaseModel):
    selector: str
    timeout_ms: int = 3000

class ScreenshotReq(BaseModel):
    path: str = "logs/last.png"

state = {
    "p": None,
    "browser": None,
    "ctx": None,
    "page": None
}

async def try_start_audio(page):
    selectors = [
        ".ytp-play-button", "button.ytp-large-play-button", 
        "button[aria-label^='Play']", "button[aria-label='Play (k)']",
        "button[title='Play (k)']", "video"
    ]
    for sel in selectors:
        try:
            if sel == "video":
                await page.evaluate("document.querySelector('video')?.play()?.catch(()=>{})")
            else:
                await page.click(sel, timeout=1500)
            return True
        except Exception:
            pass
    try:
        await page.keyboard.press("k")
        return True
    except Exception:
        return False

async def ensure_browser():
    if state["p"] is None:
        state["p"] = await async_playwright().start()
    if state["browser"] is None:
        # канал msedge, headful + autoplay
        state["browser"] = await state["p"].chromium.launch(
            channel="msedge", headless=False, args=["--autoplay-policy=no-user-gesture-required"]
        )
    if state["ctx"] is None:
        state["ctx"] = await state["browser"].new_context()
    if state["page"] is None:
        state["page"] = await state["ctx"].new_page()

@app.on_event("startup")
async def _startup():
    await ensure_browser()

@app.on_event("shutdown")
async def _shutdown():
    try:
        if state["browser"]:
            await state["browser"].close()
    finally:
        if state["p"]:
            await state["p"].stop()

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/open")
async def open_url(req: OpenReq):
    await ensure_browser()
    page = state["page"] if not req.new_tab else await state["ctx"].new_page()
    await page.goto(req.url, wait_until="domcontentloaded")
    acted = False
    if req.auto_play:
        acted = await try_start_audio(page)
    if req.duration > 0:
        await asyncio.sleep(max(1, req.duration))
    return {"ok": True, "auto_play_attempted": req.auto_play, "auto_play_action": acted}

@app.post("/play_audio")
async def play_audio(req: PlayAudioReq):
    await ensure_browser()
    page = state["page"]
    if req.page_url:
        await page.goto(req.page_url, wait_until="domcontentloaded")
    await page.evaluate("""
        url => {
          const a = new Audio(url);
          a.autoplay = true;
          a.loop = false;
          a.volume = 1.0;
          document.body.appendChild(a);
          a.play().catch(console.error);
        }
    """, req.audio_url)
    if req.duration > 0:
        await asyncio.sleep(max(1, req.duration))
    return {"ok": True}

@app.post("/click")
async def click(req: ClickReq):
    await ensure_browser()
    page = state["page"]
    try:
        await page.click(req.selector, timeout=req.timeout_ms)
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.post("/screenshot")
async def screenshot(req: ScreenshotReq):
    await ensure_browser()
    os.makedirs(os.path.dirname(req.path) or ".", exist_ok=True)
    await state["page"].screenshot(path=req.path, full_page=True)
    return {"ok": True, "path": req.path}

@app.post("/close")
async def close():
    try:
        if state["browser"]:
            await state["browser"].close()
        if state["p"]:
            await state["p"].stop()
        return {"ok": True}
    finally:
        state.update({"p": None, "browser": None, "ctx": None, "page": None})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("tools.browser_service:app", host=APP_HOST, port=APP_PORT, reload=False)
