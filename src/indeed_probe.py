"""Task B: staged, low-volume probe of vn.indeed.com to document its anti-bot measures.

Each stage makes ONE request, records the evidence, and moves on. Output: result/indeed_probe.json
Run:  python src/indeed_probe.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import httpx

URL = "https://vn.indeed.com/jobs?q=remote"
OUT = Path(__file__).resolve().parent.parent / "result"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
BROWSER_HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
    "Referer": "https://www.google.com/",
}
SIGNS = [
    "cloudflare",
    "cf-chl",
    "turnstile",
    "Just a moment",
    "captcha",
    "Access Denied",
    "challenge",
]


def summarize(name: str, status: int, headers: dict, body: str) -> dict:
    hdr_keys = ("server", "cf-ray", "cf-mitigated", "set-cookie", "content-type")
    return {
        "stage": name,
        "status": status,
        "interesting_headers": {k: headers.get(k) for k in hdr_keys if headers.get(k)},
        "signatures_found": [s for s in SIGNS if s.lower() in body.lower()],
        "job_cards_found": len(re.findall(r"data-jk=|job_seen_beacon", body)),
        "body_len": len(body),
        "title": (re.search(r"<title>(.*?)</title>", body, re.DOTALL) or [None, ""])[
            1
        ].strip(),
    }


def stage_plain_httpx() -> dict:
    r = httpx.get(URL, follow_redirects=True, timeout=20)
    return summarize("1_plain_httpx(default UA)", r.status_code, r.headers, r.text)


def stage_browser_headers() -> dict:
    r = httpx.get(URL, headers=BROWSER_HEADERS, follow_redirects=True, timeout=20)
    return summarize("2_httpx_browser_headers", r.status_code, r.headers, r.text)


def stage_playwright(headless: bool) -> dict:
    from playwright.sync_api import sync_playwright

    name = "3_playwright_headless" if headless else "4_playwright_headed"
    with sync_playwright() as p:
        b = p.chromium.launch(headless=headless)
        ctx = b.new_context(user_agent=UA, locale="vi-VN")
        page = ctx.new_page()
        resp = page.goto(URL, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(5000)
        html = page.content()
        webdriver = page.evaluate("navigator.webdriver")
        OUT.mkdir(exist_ok=True)
        page.screenshot(path=str(OUT / f"indeed_{name}.png"))
        b.close()
    d = summarize(name, resp.status if resp else -1, resp.headers if resp else {}, html)
    d["navigator.webdriver"] = webdriver
    return d


def main() -> None:
    results = []
    for fn in (
        stage_plain_httpx,
        stage_browser_headers,
        lambda: stage_playwright(True),
        lambda: stage_playwright(False),
    ):
        try:
            results.append(fn())
        except Exception as e:  # noqa: BLE001
            results.append(
                {"stage": getattr(fn, "__name__", "lambda"), "error": repr(e)}
            )
        print(json.dumps(results[-1], ensure_ascii=False, indent=2))
    OUT.mkdir(exist_ok=True)
    (OUT / "indeed_probe.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
