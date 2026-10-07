"""HTML cleaning and link ranking (generic, no per-site selectors)."""
from __future__ import annotations

import re
from typing import List, Tuple
from urllib.parse import urljoin, urldefrag, urlparse

from bs4 import BeautifulSoup

# (keyword, weight) matched against anchor text and URL path
POSITIVE = [
    ("会社概要", 10), ("企業概要", 10), ("会社情報", 8), ("企業情報", 8),
    ("会社案内", 8), ("corporate", 5), ("company", 5), ("outline", 7),
    ("profile", 6), ("overview", 6), ("about", 4), ("gaiyo", 8), ("info", 2),
    ("概要", 4), ("沿革", 1), ("コーポレート", 5),
]
NEGATIVE = [
    ("recruit", -8), ("採用", -8), ("news", -4), ("ニュース", -4), ("ir", -1),
    ("product", -4), ("商品", -4), ("製品", -4), ("contact", -5), ("お問い合わせ", -5),
    ("privacy", -6), ("プライバシー", -6), ("sitemap", -3), ("サイトマップ", -3),
    ("english", -6), ("/en/", -6), ("shop", -4), ("株主", -3), ("決算", -4),
]
SKIP_EXT = (".pdf", ".jpg", ".png", ".zip", ".xlsx", ".doc", ".docx", ".mp4")


def clean_text(html: str, max_chars: int = 12000) -> str:
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript", "nav", "header", "svg", "iframe"]):
        t.decompose()
    # Preserve table / definition-list structure as "label: value" lines.
    for tr in soup.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
        tr.replace_with(soup.new_string(" | ".join(cells) + "\n"))
    for dl in soup.find_all("dl"):
        lines = []
        for dt in dl.find_all("dt"):
            dd = dt.find_next_sibling("dd")
            lines.append(f"{dt.get_text(' ', strip=True)} : {dd.get_text(' ', strip=True) if dd else ''}")
        dl.replace_with(soup.new_string("\n".join(lines) + "\n"))
    text = soup.get_text("\n", strip=True)
    text = re.sub(r"\n{2,}", "\n", text)
    return text[:max_chars]


def registrable_domain(host: str) -> str:
    """Naive eTLD+1: keeps 3 labels for co.jp / or.jp / ne.jp style hosts, else 2."""
    parts = host.split(":")[0].split(".")
    if len(parts) >= 3 and parts[-2] in {"co", "or", "ne", "ac", "go"}:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def extract_links(html: str, base_url: str) -> List[Tuple[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    # Same registrable domain, so corporate.example.co.jp counts as the same company.
    host = registrable_domain(urlparse(base_url).netloc)
    seen, out = set(), []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        url = urldefrag(urljoin(base_url, href))[0]
        p = urlparse(url)
        if registrable_domain(p.netloc) != host or url.lower().endswith(SKIP_EXT) or url in seen:
            continue
        seen.add(url)
        out.append((a.get_text(" ", strip=True), url))
    return out


def score_link(text: str, url: str) -> int:
    hay = (text + " " + urlparse(url).path).lower()
    s = 0
    for kw, w in POSITIVE + NEGATIVE:
        if kw.lower() in hay:
            s += w
    return s


def rank_links(links: List[Tuple[str, str]], top_n: int = 5) -> List[Tuple[str, str, int]]:
    scored = [(t, u, score_link(t, u)) for t, u in links]
    scored = [x for x in scored if x[2] > 0]
    scored.sort(key=lambda x: -x[2])
    return scored[:top_n]
