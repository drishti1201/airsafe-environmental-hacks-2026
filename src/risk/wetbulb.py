"""Wet-bulb temperature and hourly heat-stress classification.

Wet-bulb temperature (Tw) combines air temperature and humidity. It shows how
well sweat can evaporate, which is what lets the body cool itself. Plain air
temperature misses this: 36 C at 80% humidity is more dangerous than 40 C at
20% humidity.

Formula: Stull (2011), "Wet-Bulb Temperature from Relative Humidity and Air
Temperature", J. Appl. Meteorol. Climatol. Valid for RH 5-99% and T -20..50 C,
accurate to about +/- 1 C. Cite this in the README.

THRESHOLDS ARE PLACEHOLDERS TO VERIFY. 28 C (watch) and 31 C (danger) are
common planning values from heat-stress literature. Confirm them against a
source you can cite (for example IMD / NDMA heat guidance, or published
wet-bulb limits for sustained exposure) before the demo, and state them in the
README as "illustrative thresholds, not clinical advice".
"""

from math import atan, sqrt

WATCH_C = 28.0   # verify before submission
DANGER_C = 31.0  # verify before submission


def wet_bulb_c(temp_c: float, rh_percent: float) -> float:
    """Stull approximation. temp_c in Celsius, rh_percent in 0-100."""
    rh = max(5.0, min(99.0, rh_percent))  # keep inside the formula's valid range
    t = temp_c
    return (
        t * atan(0.151977 * sqrt(rh + 8.313659))
        + atan(t + rh)
        - atan(rh - 1.676331)
        + 0.00391838 * rh ** 1.5 * atan(0.023101 * rh)
        - 4.686035
    )


def severity_from_wet_bulb(tw_c: float) -> int:
    """0 = low, 1 = elevated, 2 = watch, 3 = danger."""
    if tw_c >= DANGER_C:
        return 3
    if tw_c >= WATCH_C:
        return 2
    if tw_c >= WATCH_C - 2:
        return 1
    return 0


def analyse_forecast(hourly):
    """hourly: list of dicts {"hour": 0-23, "temp_c": float, "rh": float}.

    Returns the peak hour, its wet-bulb value and severity, plus the full
    curve (for the "why this score" chart).
    """
    if not hourly:
        raise ValueError("empty forecast")
    curve = [
        {
            "hour": h["hour"],
            "temp_c": h["temp_c"],
            "rh": h["rh"],
            "wet_bulb_c": round(wet_bulb_c(h["temp_c"], h["rh"]), 1),
        }
        for h in hourly
    ]
    peak = max(curve, key=lambda p: p["wet_bulb_c"])
    return {
        "peak_hour": peak["hour"],
        "peak_wet_bulb_c": peak["wet_bulb_c"],
        "peak_temp_c": peak["temp_c"],
        "peak_rh": peak["rh"],
        "severity": severity_from_wet_bulb(peak["wet_bulb_c"]),
        "curve": curve,
    }
