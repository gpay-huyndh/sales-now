"""LLM extraction via litellm (provider-agnostic: Gemini / OpenAI / Anthropic / Ollama)."""
from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, Optional

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

FIELDS = ["head_office_address", "representative_name", "representative_title", "capital", "established"]
USAGE = {"prompt_tokens": 0, "completion_tokens": 0, "cost": 0.0, "calls": 0}


def model_name() -> str:
    return os.getenv("LLM_MODEL", "gemini/gemini-2.0-flash")


def _parse_json(s: str) -> Optional[Dict[str, Any]]:
    m = re.search(r"\{.*\}", s, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def extract(company: str, page_text: str) -> Optional[Dict[str, Any]]:
    resp = litellm.completion(
        model=model_name(),
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Company: {company}\n\nPAGE TEXT:\n{page_text}"},
        ],
    )
    u = getattr(resp, "usage", None)
    if u:
        USAGE["prompt_tokens"] += u.prompt_tokens or 0
        USAGE["completion_tokens"] += u.completion_tokens or 0
    try:
        USAGE["cost"] += litellm.completion_cost(completion_response=resp) or 0.0
    except Exception:
        pass
    USAGE["calls"] += 1
    return _parse_json(resp.choices[0].message.content or "")
