"""Validation and normalisation of extracted fields."""
from __future__ import annotations

import re
from typing import Any, Dict, Optional

ERAS = {"明治": 1868, "大正": 1912, "昭和": 1926, "平成": 1989, "令和": 2019}
_Z2H = str.maketrans("０１２３４５６７８９", "0123456789")


def normalize_established(s: Optional[str]) -> Optional[str]:
    """Return YYYY-MM from strings like '1943年3月', '昭和18年3月', '1943/03'."""
    if not s:
        return None
    s = s.translate(_Z2H)
    m = re.search(r"(明治|大正|昭和|平成|令和)\s*(元|\d+)\s*年\s*(\d{1,2})\s*月", s)
    if m:
        y = 1 if m.group(2) == "元" else int(m.group(2))
        return f"{ERAS[m.group(1)] + y - 1:04d}-{int(m.group(3)):02d}"
    m = re.search(r"(\d{4})\s*[年/.\-]\s*(\d{1,2})", s)
    if m:
        return f"{int(m.group(1)):04d}-{int(m.group(2)):02d}"
    return None


def valid_address(s: Optional[str]) -> bool:
    return bool(s) and bool(re.search(r"[都道府県]", s))


def valid_capital(s: Optional[str]) -> bool:
    return bool(s) and bool(re.search(r"\d", s.translate(_Z2H))) and "円" in s


def evidence_in_text(evidence: Optional[Dict[str, str]], text: str) -> Dict[str, bool]:
    """Anti-hallucination check: quoted snippet must appear (whitespace-insensitive)."""
    squash = lambda x: re.sub(r"\s+", "", x or "")
    t = squash(text)
    return {k: squash(v)[:20] in t for k, v in (evidence or {}).items() if v}


def normalize(rec: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(rec)
    out["established_raw"] = rec.get("established")
    out["established"] = normalize_established(rec.get("established"))
    if not valid_address(out.get("head_office_address")):
        out["head_office_address"] = None
    if not valid_capital(out.get("capital")):
        out["capital"] = None
    return out


def missing_fields(rec: Dict[str, Any]) -> list:
    return [k for k in ("head_office_address", "representative_name", "capital", "established") if not rec.get(k)]
