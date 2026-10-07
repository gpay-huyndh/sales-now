import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from normalizer import normalize_established, valid_address, valid_capital  # noqa: E402
from page_parser import score_link  # noqa: E402


def test_established():
    assert normalize_established("1943年3月") == "1943-03"
    assert normalize_established("昭和18年3月") == "1943-03"
    assert normalize_established("平成元年4月") == "1989-04"
    assert normalize_established("２０００年１０月") == "2000-10"
    assert normalize_established("不明") is None


def test_validators():
    assert valid_address("東京都港区西新橋1-3-1")
    assert not valid_address("港区")
    assert valid_capital("100億円")
    assert not valid_capital("なし")


def test_link_score():
    assert score_link("会社概要", "/company/outline/") > score_link("採用情報", "/recruit/")
