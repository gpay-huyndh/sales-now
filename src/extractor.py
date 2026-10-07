"""LLM extraction via litellm (provider-agnostic: Gemini / OpenAI / Anthropic / Ollama)."""

from __future__ import annotations

import json
import os
import re
import time
from typing import Any

import litellm

litellm.drop_params = True

SYSTEM_PROMPT = """You extract corporate facts from Japanese company web pages.
Return ONLY a JSON object with keys:
  head_office_address, representative_name, representative_title, capital, established,
  evidence (object mapping each non-null field to the exact quoted source snippet).
Rules:
- Use only information explicitly present in the text. If absent, use null. Never guess.
- head_office_address: the head office / 本社所在地 (not branches, factories, or labs).
- representative_name: the 代表取締役 (President/CEO) personal name, without title.
- capital: keep the original text, e.g. "100億円".
- established: 設立年月 as written (e.g. "1943年3月") or YYYY-MM if given in Western calendar.
"""

FIELDS = [
    "head_office_address",
    "representative_name",
    "representative_title",
    "capital",
    "established",
]
USAGE = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "cost": 0.0,
    "calls": 0,
    "models_used": {},
}
LAST_CALL: dict[
    str, Any
] = {}  # usage of the most recent call (read by main.py per company)


def model_name() -> str:
    return os.getenv("LLM_MODEL", "gemini/gemini-3.8-flash")


def _parse_json(s: str) -> dict[str, Any] | None:
    m = re.search(r"\{.*\}", s, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def _completion(model: str, messages: list):
    print(f"    -> LLM call ({model}) ...", flush=True)
    time.sleep(
        4.5
    )  # Throttle to ~13 requests per minute to stay under the 15 RPM limit
    t0 = time.time()
    resp = litellm.completion(
        model=model,
        temperature=0,
        messages=messages,
        timeout=60,  # never hang silently
        num_retries=2,  # backoff on 429/503
    )
    print(f"    <- done in {time.time() - t0:.1f}s", flush=True)
    return resp


def extract(company: str, page_text: str) -> dict[str, Any] | None:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Company: {company}\n\nPAGE TEXT:\n{page_text}"},
    ]
    try:
        resp = _completion(model_name(), messages)
    except (
        litellm.ServiceUnavailableError,
        litellm.RateLimitError,
        litellm.InternalServerError,
        litellm.Timeout,
        litellm.NotFoundError,
    ):
        fb = os.getenv("LLM_FALLBACK_MODEL")
        if not fb:
            raise
        print(f"    primary model failed, falling back to {fb}", flush=True)
        resp = _completion(fb, messages)
    u = getattr(resp, "usage", None)
    pt = (u.prompt_tokens or 0) if u else 0
    ct = (u.completion_tokens or 0) if u else 0
    USAGE["prompt_tokens"] += pt
    USAGE["completion_tokens"] += ct
    cost = 0.0
    try:
        cost = litellm.completion_cost(completion_response=resp) or 0.0
    except Exception:  # noqa: BLE001, S110
        pass
    USAGE["cost"] += cost
    USAGE["calls"] += 1
    used = getattr(resp, "model", None) or model_name()
    USAGE["models_used"][used] = USAGE["models_used"].get(used, 0) + 1
    LAST_CALL.update(model=used, prompt_tokens=pt, completion_tokens=ct, cost=cost)
    return _parse_json(resp.choices[0].message.content or "")
