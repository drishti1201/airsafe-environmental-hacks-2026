"""Household heat-risk scoring and Hindi briefing.

score = weather severity (0-3, from peak wet-bulb) x vulnerability points.
Everything here is rule-based and deterministic, so the briefing can never
invent a reason. Weights are illustrative; document them in the README.
"""

from .wetbulb import analyse_forecast

# (field check, points, English reason, Hindi reason)
VULNERABILITY_RULES = [
    (lambda h: h["age_group"] == "65+", 3, "age 65+", "65 साल से ऊपर के बुजुर्ग"),
    (lambda h: h["age_group"] == "infant", 3, "infant under 2", "2 साल से छोटा बच्चा"),
    (lambda h: h.get("pregnant", False), 2, "pregnant", "गर्भवती महिला"),
    (lambda h: h.get("lives_alone", False), 2, "lives alone", "अकेले रहते हैं"),
    (lambda h: h.get("outdoor_worker", False), 2, "outdoor worker", "बाहर धूप में काम करते हैं"),
    (lambda h: h.get("roof_type") in ("tin", "asbestos"), 1, "tin/asbestos roof", "टिन/एस्बेस्टस की छत"),
]

HIGH_AT = 9      # e.g. danger-level day (3) x 3 points
MEDIUM_AT = 4


def vulnerability(household):
    points, en, hi = 0, [], []
    for check, pts, reason_en, reason_hi in VULNERABILITY_RULES:
        if check(household):
            points += pts
            en.append(reason_en)
            hi.append(reason_hi)
    return points, en, hi


def band(score):
    if score >= HIGH_AT:
        return "High"
    if score >= MEDIUM_AT:
        return "Medium"
    return "Low"


def score_household(household, analysis):
    pts, en, hi = vulnerability(household)
    score = analysis["severity"] * pts
    return {
        **household,
        "vulnerability_points": pts,
        "score": score,
        "risk": band(score),
        "reason_en": ", ".join(en) if en else "no major risk factors",
        "reason_hi": ", ".join(hi) if hi else "कोई बड़ा जोखिम कारक नहीं",
        "peak_hour": analysis["peak_hour"],
        "peak_wet_bulb_c": analysis["peak_wet_bulb_c"],
    }


def rank_households(households, hourly_forecast, mitanin_id=None):
    """Return (analysis, ranked list, highest score first)."""
    analysis = analyse_forecast(hourly_forecast)
    pool = [h for h in households if mitanin_id is None or h["mitanin_id"] == mitanin_id]
    ranked = sorted(
        (score_household(h, analysis) for h in pool),
        key=lambda r: (-r["score"], r["id"]),
    )
    return analysis, ranked


def _hour_hi(hour):
    h12 = hour % 12 or 12
    return f"{h12} बजे"


def build_briefing_hi(analysis, ranked, top_n=5):
    """Fixed Hindi template. Feed the returned string to Polly (Hindi voice)."""
    sev = analysis["severity"]
    if sev == 0:
        return "कल गर्मी का खतरा कम है। सामान्य दौरा जारी रखें।"

    level = {1: "थोड़ा बढ़ा हुआ", 2: "चेतावनी स्तर पर", 3: "खतरनाक स्तर पर"}[sev]
    lines = [
        f"कल {_hour_hi(analysis['peak_hour'])} के आसपास गर्मी और नमी {level} रहेगी।",
        f"तापमान लगभग {round(analysis['peak_temp_c'])} डिग्री और नमी {round(analysis['peak_rh'])} प्रतिशत है।",
    ]
    urgent = [r for r in ranked if r["risk"] in ("High", "Medium")][:top_n]
    if not urgent:
        lines.append("आज किसी घर को खास खतरा नहीं है।")
    else:
        lines.append(f"सबसे पहले इन {len(urgent)} घरों में जाएँ।")
        for i, r in enumerate(urgent, 1):
            lines.append(f"{i}. {r['name']}, वार्ड {r['ward']}। कारण: {r['reason_hi']}।")
        lines.append("पानी, ओआरएस और छाँव की सलाह दें।")
    return " ".join(lines)


if __name__ == "__main__":
    # quick manual check: python -m src.risk.scoring
    import json
    from pathlib import Path

    data = json.loads((Path(__file__).parents[2] / "data" / "households.json").read_text(encoding="utf-8"))
    hot_day = [{"hour": h, "temp_c": t, "rh": r} for h, t, r in
               [(9, 33, 60), (11, 37, 55), (13, 39, 50), (15, 38, 52), (17, 35, 58)]]
    analysis, ranked = rank_households(data, hot_day, mitanin_id="M01")
    print("peak:", analysis["peak_hour"], analysis["peak_wet_bulb_c"], "severity", analysis["severity"])
    for r in ranked[:5]:
        print(r["id"], r["risk"], r["score"], "|", r["reason_en"])
    print()
    print(build_briefing_hi(analysis, ranked))
