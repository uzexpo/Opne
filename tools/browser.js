const { chromium } = require('playwright');

(async () => {
  const args = process.argv.slice(2);
  const get = (flag) => { const i = args.indexOf(flag); return i >= 0 ? args[i+1] : null; };
  const open = get('--open');
  const audio = get('--play-audio-url');
  const click = get('--click');
  const duration = parseInt(get('--duration') || '10', 10);

  const browser = await chromium.launch({ channel: 'msedge', headless: false, args: ['--autoplay-policy=no-user-gesture-required']});
  const page = await browser.newPage();
  if (open) await page.goto(open, { waitUntil: 'domcontentloaded' });
  if (click) { try { await page.click(click, { timeout: 5000 }); } catch(e){ console.log('WARN CLICK:', e.message); } }
  if (audio) {
    await page.evaluate((url) => {
      const a = new Audio(url); a.autoplay = true; a.volume = 1.0; document.body.appendChild(a); a.play().catch(console.error);
    }, audio);
  }
  await new Promise(r => setTimeout(r, Math.max(1000, duration*1000)));
  await browser.close();
  console.log('OK: browser task done');
})();
