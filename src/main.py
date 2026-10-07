"""CLI: crawl each company site, find the company-outline pages, extract fields with an LLM."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))

import extractor
from fetcher import fetch
from normalizer import evidence_in_text, missing_fields, normalize
from page_parser import clean_text, extract_links, rank_links

ROOT = Path(__file__).resolve().parent.parent
FIELDS = [
    "head_office_address",
    "representative_name",
    "representative_title",
    "capital",
    "established",
]


def candidate_pages(top_url: str, max_pages: int, depth2: bool = True):
    """Return ranked candidate URLs: depth-1 from the top page, then depth-2 from the best hit."""
    html = fetch(top_url)
    if not html:
        return []
    ranked = rank_links(extract_links(html, top_url), top_n=max_pages)
    urls = [(u, s) for _, u, s in ranked]
    if depth2 and ranked:
        # e.g. 企業情報 -> 会社概要
        h2 = fetch(ranked[0][1])
        if h2:
            for _, u, s in rank_links(extract_links(h2, ranked[0][1]), top_n=max_pages):
                if u not in [x[0] for x in urls]:
                    urls.append((u, s + 1))
    urls.sort(key=lambda x: -x[1])
    return [u for u, _ in urls][: max_pages * 2]


def process(name: str, url: str, max_pages: int) -> dict:
    t0 = time.time()
    rec = {
        "company": name,
        "url": url,
        **{f: None for f in FIELDS},
        "source_url": None,
        "verified": {},
        "model": None,
        "llm_calls": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "cost_usd": 0.0,
    }
    visited = []
    for page_url in candidate_pages(url, max_pages):
        html = fetch(page_url)
        if not html:
            continue
        text = clean_text(html)
        visited.append(page_url)
        try:
            got = extractor.extract(name, text)
            lc = extractor.LAST_CALL
            rec["model"] = lc.get("model")
            rec["llm_calls"] += 1
            rec["prompt_tokens"] += lc.get("prompt_tokens", 0)
            rec["completion_tokens"] += lc.get("completion_tokens", 0)
            rec["cost_usd"] = round(rec["cost_usd"] + lc.get("cost", 0.0), 6)
        except Exception as e:  # noqa: BLE001, network / quota errors should not kill the batch
            print(f"  LLM error: {e}", file=sys.stderr)
            continue
        if not got:
            continue
        got = normalize(got)
        v = evidence_in_text(got.get("evidence"), text)
        for f in FIELDS:
            # fill only missing fields; drop values whose evidence is not in the page
            if rec[f] is None and got.get(f) and v.get(f, True):
                rec[f] = got[f]
                rec["verified"][f] = v.get(f, None)
                rec["source_url"] = rec["source_url"] or page_url
        rec["established"] = rec["established"]
        if not missing_fields(rec):
            break
    rec["pages_visited"] = visited
    rec["pages_count"] = len(visited)
    rec["seconds"] = round(time.time() - t0, 1)
    return rec


def main() -> None:
    load_dotenv(ROOT / ".env")
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=str(ROOT / "input" / "companies.csv"))
    ap.add_argument("--out", default=str(ROOT / "result"))
    ap.add_argument("--max-pages", type=int, default=4)
    ap.add_argument(
        "--only", help="process only companies whose name contains this string"
    )
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(exist_ok=True)
    with open(a.input, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if a.only:
        rows = [r for r in rows if a.only in r["name"]]

    results = []
    for r in rows:
        print(f"[{r['name']}] {r['url']}")
        rec = process(r["name"], r["url"], a.max_pages)
        print(
            f"  -> {rec['head_office_address']} / {rec['representative_name']} / "
            f"{rec['capital']} / {rec['established']} ({rec['seconds']}s)"
        )
        results.append(rec)

    (out / "companies.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    cols = [
        "company",
        "url",
        *FIELDS,
        "source_url",
        "model",
        "llm_calls",
        "prompt_tokens",
        "completion_tokens",
        "cost_usd",
        "pages_count",
        "seconds",
    ]
    with open(out / "companies.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)
    (out / "run_log.json").write_text(
        json.dumps(
            {
                "model": extractor.model_name(),
                "usage": extractor.USAGE,
                "total_seconds": round(sum(r["seconds"] for r in results), 1),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("done:", extractor.USAGE)


if __name__ == "__main__":
    main()
