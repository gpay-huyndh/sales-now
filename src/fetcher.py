"""Page fetching: fast httpx first, Playwright fallback for JS-rendered pages."""

from __future__ import annotations

import hashlib
import time
from pathlib import Path

import httpx

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
HEADERS = {"User-Agent": UA, "Accept-Language": "ja,en;q=0.8"}
MIN_TEXT_LEN = 300  # below this we assume the page needs JS rendering


def _cache_path(url: str) -> Path:
    return CACHE_DIR / (hashlib.md5(url.encode()).hexdigest() + ".html")


def _decode(resp: httpx.Response) -> str:
    # Many JP sites still serve Shift_JIS / EUC-JP; let httpx guess then fall back.
    try:
        return resp.text
    except Exception:  # noqa: BLE001
        return resp.content.decode("utf-8", errors="ignore")


def fetch_httpx(url: str, retries: int = 2, timeout: float = 20.0) -> str | None:
    for attempt in range(retries + 1):
        try:
            with httpx.Client(
                headers=HEADERS, follow_redirects=True, timeout=timeout
            ) as c:
                r = c.get(url)
            if r.status_code == 200:
                return _decode(r)
            if r.status_code in (403, 429, 503):
                return None
        except httpx.HTTPError:
            pass
        time.sleep(1.5 * (attempt + 1))
    return None


def fetch_playwright(url: str, timeout_ms: int = 30000) -> str | None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx = browser.new_context(user_agent=UA, locale="ja-JP")
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            html = page.content()
            browser.close()
            return html
    except Exception:  # noqa: BLE001
        return None


def fetch(url: str, use_cache: bool = True, delay: float = 0.5) -> str | None:
    """Fetch HTML with cache; fall back to a headless browser when content is thin."""
    CACHE_DIR.mkdir(exist_ok=True)
    cp = _cache_path(url)
    if use_cache and cp.exists():
        return cp.read_text(encoding="utf-8", errors="ignore")

    time.sleep(delay)  # be polite
    html = fetch_httpx(url)
    if html is None or len(html) < MIN_TEXT_LEN:
        html = fetch_playwright(url) or html
    if html:
        cp.write_text(html, encoding="utf-8")
    return html
