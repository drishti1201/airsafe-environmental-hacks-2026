"""Run from the repo root:  python -m pytest tests -q   (or: python tests/test_risk.py)"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.risk.wetbulb import wet_bulb_c, severity_from_wet_bulb, analyse_forecast
from src.risk.scoring import score_household, rank_households, build_briefing_hi


def test_wet_bulb_matches_stull_example():
    # Stull (2011) worked example: T=20 C, RH=50% -> Tw about 13.7 C
    assert abs(wet_bulb_c(20, 50) - 13.7) < 0.3


def test_humidity_matters_more_than_air_temp():
    # humid 36 C is more dangerous than dry 40 C
    assert wet_bulb_c(36, 80) > wet_bulb_c(40, 20)


def test_severity_bands():
    assert severity_from_wet_bulb(20) == 0
    assert severity_from_wet_bulb(27) == 1
    assert severity_from_wet_bulb(29) == 2
    assert severity_from_wet_bulb(32) == 3


def test_same_day_different_households():
    hot = [{"hour": 13, "temp_c": 39, "rh": 55}]
    analysis = analyse_forecast(hot)
    assert analysis["severity"] == 3
    elder = {"id": "A", "age_group": "65+", "lives_alone": True, "roof_type": "tin",
             "pregnant": False, "outdoor_worker": False}
    adult = {"id": "B", "age_group": "adult", "lives_alone": False, "roof_type": "concrete",
             "pregnant": False, "outdoor_worker": False}
    assert score_household(elder, analysis)["risk"] == "High"
    assert score_household(adult, analysis)["risk"] == "Low"


def test_cool_day_ranks_everyone_low():
    cool = [{"hour": 13, "temp_c": 25, "rh": 40}]
    hh = [{"id": "A", "mitanin_id": "M01", "age_group": "65+", "lives_alone": True,
           "roof_type": "tin", "pregnant": False, "outdoor_worker": False,
           "name": "x", "ward": "12"}]
    analysis, ranked = rank_households(hh, cool)
    assert ranked[0]["risk"] == "Low"
    assert "कम" in build_briefing_hi(analysis, ranked)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
