"""Mitanin Heat Desk: single Lambda behind a Function URL.

Routes
  GET  /?mitanin=M01            ranked households + Hindi briefing (+ audio URL)
  GET  /?mitanin=M01&demo=hot   same, but with a SIMULATED hot humid day
  POST /visit                   body {"household_id": "H011", "status": "visited"}

Environment variables (all optional except where noted)
  BUCKET        S3 bucket for briefing audio. If unset, audio is skipped.
  TABLE         DynamoDB table for visit log (PK household_id, SK date). If unset, visits are not stored.
  POLLY_VOICE   default "Kajal" (hi-IN, neural). Falls back to "Aditi" (standard) on error.
  POLLY_REGION  region for Polly if Mumbai lacks your voice, e.g. "us-east-1"
  LAT / LON     forecast location, default Raipur (21.25, 81.63)

CORS: set it on the Function URL itself (console -> Configuration -> Function URL -> CORS),
not in this code, otherwise the browser sees duplicate headers.
"""

import json
import os
import sys
import urllib.request
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Works both inside the Lambda zip (risk/ next to this file) and locally (src/risk).
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from risk.scoring import rank_households, build_briefing_hi

IST = timezone(timedelta(hours=5, minutes=30))
LAT = float(os.environ.get("LAT", "21.25"))
LON = float(os.environ.get("LON", "81.63"))

# Simulated day for demos when the real forecast is mild. Always labelled "simulated".
DEMO_HOT_DAY = [
    {"hour": h, "temp_c": t, "rh": r}
    for h, t, r in [(9, 34, 68), (11, 37, 66), (13, 38, 68), (15, 37, 66), (17, 35, 70)]
]

DEMO_COOL_DAY = [
    {"hour": h, "temp_c": t, "rh": r}
    for h, t, r in [
        (9, 24, 45),
        (11, 27, 42),
        (13, 29, 40),
        (15, 28, 43),
        (17, 25, 48),
    ]
]


def _households():
    for p in (HERE / "households.json", HERE.parent.parent / "data" / "households.json"):
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    raise FileNotFoundError("households.json not found")


def fetch_tomorrow_forecast():
    """Open-Meteo hourly temp + humidity for tomorrow, daytime hours 9-18 IST."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&hourly=temperature_2m,relative_humidity_2m"
        "&timezone=Asia%2FKolkata&forecast_days=3"
    )
    with urllib.request.urlopen(url, timeout=8) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    tomorrow = (datetime.now(IST) + timedelta(days=1)).strftime("%Y-%m-%d")
    out = []
    for ts, t, rh in zip(
        data["hourly"]["time"],
        data["hourly"]["temperature_2m"],
        data["hourly"]["relative_humidity_2m"],
    ):
        if ts.startswith(tomorrow):
            hour = int(ts[11:13])
            if 9 <= hour <= 18 and t is not None and rh is not None:
                out.append({"hour": hour, "temp_c": t, "rh": rh})
    if not out:
        raise RuntimeError("no forecast rows for tomorrow")
    return out


def synth_audio(text):
    """Hindi text -> MP3 in S3 -> presigned URL. Returns None if BUCKET unset or Polly fails."""
    bucket = os.environ.get("BUCKET")
    if not bucket:
        return None
    import boto3  # available in the Lambda runtime

    region = os.environ.get("POLLY_REGION")
    polly = boto3.client("polly", region_name=region) if region else boto3.client("polly")
    text = text[:2900]  # synchronous Polly limit guard
    attempts = [
        (os.environ.get("POLLY_VOICE", "Kajal"), "neural"),
        ("Aditi", "standard"),
    ]
    audio = None
    for voice, engine in attempts:
        try:
            r = polly.synthesize_speech(
                Text=text, OutputFormat="mp3", VoiceId=voice, Engine=engine, LanguageCode="hi-IN"
            )
            audio = r["AudioStream"].read()
            break
        except Exception as e:  # try the fallback voice
            print("polly failed", voice, engine, repr(e))
    if audio is None:
        return None
    s3 = boto3.client("s3")
    key = f"briefings/{datetime.now(IST):%Y-%m-%d}/{uuid.uuid4().hex}.mp3"
    s3.put_object(Bucket=bucket, Key=key, Body=audio, ContentType="audio/mpeg")
    return s3.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=3600
    )


def log_visit(body):
    table = os.environ.get("TABLE")
    if not table:
        return False
    import boto3

    boto3.resource("dynamodb").Table(table).put_item(
        Item={
            "household_id": body["household_id"],
            "date": datetime.now(IST).strftime("%Y-%m-%d"),
            "status": body.get("status", "visited"),
            "ors_given": bool(body.get("ors_given", False)),
            "logged_at": datetime.now(IST).isoformat(),
        }
    )
    return True


def _resp(code, payload):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json; charset=utf-8"},
        "body": json.dumps(payload, ensure_ascii=False),
    }


def handler(event, context=None):
    http = event.get("requestContext", {}).get("http", {})
    method = http.get("method", "GET")
    path = event.get("rawPath", "/")
    qs = event.get("queryStringParameters") or {}

    try:
        if method == "POST" and path.rstrip("/").endswith("/visit"):
            body = json.loads(event.get("body") or "{}")
            if not body.get("household_id"):
                return _resp(400, {"error": "household_id required"})
            return _resp(200, {"ok": True, "stored": log_visit(body)})

        if method != "GET":
            return _resp(405, {"error": "method not allowed"})

        mitanin = qs.get("mitanin")
        if not mitanin:
            return _resp(400, {"error": "mitanin query parameter required, e.g. ?mitanin=M01"})

        if qs.get("demo") == "hot":
            forecast, source = DEMO_HOT_DAY, "simulated"
        elif qs.get("demo") == "cool":
            forecast, source = DEMO_COOL_DAY, "simulated"
        else:
            forecast, source = fetch_tomorrow_forecast(), "open-meteo"

        selected_mitanin = None if mitanin == "ALL" else mitanin
        analysis, ranked = rank_households(
            _households(), forecast, mitanin_id=selected_mitanin
        )
        briefing = build_briefing_hi(analysis, ranked)
        return _resp(
            200,
            {
                "forecast_source": source,
                "mitanin_id": mitanin,
                "analysis": analysis,
                "households": ranked,
                "briefing_hi": briefing,
                "audio_url": synth_audio(briefing),
            },
        )
    except Exception as e:
        print("error", repr(e))
        return _resp(500, {"error": "internal error", "detail": str(e)[:200]})


if __name__ == "__main__":
    # local smoke test, no AWS needed: python src/lambda/handler.py
    ev = {"requestContext": {"http": {"method": "GET"}}, "rawPath": "/",
          "queryStringParameters": {"mitanin": "M01", "demo": "hot"}}
    r = handler(ev)
    body = json.loads(r["body"])
    print(r["statusCode"], body["forecast_source"], "severity", body["analysis"]["severity"],
          "peak wet-bulb", body["analysis"]["peak_wet_bulb_c"])
    print([ (h["id"], h["risk"]) for h in body["households"][:5] ])
    print(body["briefing_hi"][:160], "...")
    print("audio_url:", body["audio_url"])
