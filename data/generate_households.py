"""Generate SYNTHETIC households for the demo. No real people or health data.

Run:  python data/generate_households.py
Writes data/households.json (200 households, 5 Mitanins x 40 households).
State "synthetic data" clearly in the README and in the video.
"""

import json
import random
from pathlib import Path

random.seed(42)  # reproducible

FIRST = ["सुनीता", "कमला", "रामू", "गीता", "मोहन", "लक्ष्मी", "सरिता", "दिनेश",
         "पार्वती", "राजेश", "अनीता", "भगवती", "संतोष", "मंजू", "कविता", "हरि"]
LAST = ["साहू", "यादव", "वर्मा", "कुर्रे", "ठाकुर", "निषाद", "पटेल", "सोनी"]
WARDS = ["12", "13", "14", "15", "16"]


def make_household(i, mitanin_id):
    age_group = random.choices(
        ["infant", "child", "adult", "65+"], weights=[8, 17, 55, 20]
    )[0]
    lives_alone = random.random() < (0.35 if age_group == "65+" else 0.05)
    pregnant = age_group == "adult" and random.random() < 0.10
    outdoor_worker = age_group == "adult" and random.random() < 0.40
    roof_type = random.choices(["concrete", "tin", "asbestos", "tile"], weights=[35, 35, 10, 20])[0]
    return {
        "id": f"H{i:03d}",
        "name": f"{random.choice(FIRST)} {random.choice(LAST)}",
        "mitanin_id": mitanin_id,
        "ward": random.choice(WARDS),
        "age_group": age_group,
        "lives_alone": lives_alone,
        "pregnant": pregnant,
        "outdoor_worker": outdoor_worker,
        "roof_type": roof_type,
    }


def main():
    households, n = [], 1
    for m in range(1, 6):
        for _ in range(40):
            households.append(make_household(n, f"M{m:02d}"))
            n += 1
    out = Path(__file__).parent / "households.json"
    out.write_text(json.dumps(households, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {len(households)} synthetic households to {out}")


if __name__ == "__main__":
    main()
