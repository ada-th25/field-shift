"""Tests for the NASA POWER client's handling of missing (-999) values,
added after a live request against the server's default (rolling,
today-based) date window crashed: ALLSKY_SFC_SW_DWN's real-world reporting
lag sometimes exceeds the 7-day buffer schemas.py assumes, so the most
recent day can still come back as -999 even with that buffer applied.
Downstream maths (et0_penman_monteith) can't handle a leftover NaN, so the
client now forward-fills across these gaps instead of leaving them for the
caller to trip over. Uses a pre-seeded cache file so this doesn't depend on
POWER's live, sometimes-flaky response."""
import json

import app.data.nasa_power as nasa_power_module
from app.data.nasa_power import fetch_power_daily

FIELDS = [
    "T2M_MAX", "T2M_MIN", "T2M", "RH2M", "WS2M",
    "ALLSKY_SFC_SW_DWN", "PRECTOTCORR", "GWETROOT", "GWETTOP",
]


def _raw_response(trailing_missing_field: str | None = None):
    dates = ["20230101", "20230102", "20230103"]
    parameter = {}
    for field in FIELDS:
        values = {d: 10.0 + i for i, d in enumerate(dates)}
        if field == trailing_missing_field:
            values[dates[-1]] = -999
        parameter[field] = values
    return {"properties": {"parameter": parameter}}


def _isolate_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(nasa_power_module, "CACHE_DIR", tmp_path)


def test_trailing_missing_value_is_forward_filled(tmp_path, monkeypatch):
    _isolate_cache(tmp_path, monkeypatch)
    cache_file = tmp_path / "power_42.03_-93.63_20230101_20230103.json"
    cache_file.write_text(json.dumps(_raw_response(trailing_missing_field="ALLSKY_SFC_SW_DWN")))

    df = fetch_power_daily(42.03, -93.63, start="20230101", end="20230103")

    assert not df["ALLSKY_SFC_SW_DWN"].isna().any()
    assert df["ALLSKY_SFC_SW_DWN"].iloc[-1] == df["ALLSKY_SFC_SW_DWN"].iloc[-2]


def test_no_missing_values_left_unchanged(tmp_path, monkeypatch):
    _isolate_cache(tmp_path, monkeypatch)
    cache_file = tmp_path / "power_42.03_-93.63_20230101_20230103.json"
    cache_file.write_text(json.dumps(_raw_response(trailing_missing_field=None)))

    df = fetch_power_daily(42.03, -93.63, start="20230101", end="20230103")

    assert not df.isna().any().any()
    assert df["T2M"].tolist() == [10.0, 11.0, 12.0]
