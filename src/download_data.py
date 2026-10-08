import requests
import pandas as pd
import os

import os

API_KEY = os.getenv("OPENAQ_API_KEY")

sensors = {
    "pm25": 12237394,
    "pm10": 12237393,
    "no2": 12237391,
    "o3": 12237392,
    "temperature": 12237397,
    "humidity": 12237395,
    "so2": 12237396,
    "wind_speed": 14342183,
    "wind_direction": 14342182
}

start_date = "2026-07-01T00:00:00Z"
end_date = "2026-10-08T23:59:59Z"

headers = {
    "X-API-Key": API_KEY
}

all_data = []

for parameter, sensor_id in sensors.items():

    print(f"\nDownloading {parameter}...")

    page = 1

    while True:

        url = f"https://api.openaq.org/v3/sensors/{sensor_id}/hours"

        params = {
            "datetime_from": start_date,
            "datetime_to": end_date,
            "limit": 1000,
            "page": page
        }

        response = requests.get(
            url,
            headers=headers,
            params=params
        )

        print(f"Page {page} | Status: {response.status_code}")

        if response.status_code != 200:
            print(response.text)
            break

        data = response.json()

        results = data["results"]

        if not results:
            break

        for item in results:

            if item.get("value") is not None:

                all_data.append({
                    "datetime": item["period"]["datetimeFrom"]["utc"],
                    "parameter": parameter,
                    "value": item["value"]
                })

        if len(results) < 1000:
            break

        page += 1


# Convert to dataframe
df = pd.DataFrame(all_data)

# Remove duplicate records
df = df.drop_duplicates()

# Convert datetime
df["datetime"] = pd.to_datetime(df["datetime"])

# Convert parameters into columns
df = df.pivot_table(
    index="datetime",
    columns="parameter",
    values="value",
    aggfunc="mean"
).reset_index()

# Create data folder
os.makedirs("data", exist_ok=True)

# Save final dataset
df.to_csv(
    "data/airsafe_dataset.csv",
    index=False
)

print("\n==============================")
print("DOWNLOAD COMPLETE!")
print("==============================")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nSaved as:")
print("data/airsafe_dataset.csv")