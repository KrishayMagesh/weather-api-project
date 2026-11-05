from datetime import date, timedelta

import matplotlib
import pandas as pd
import requests

matplotlib.use("Agg")  # save charts to files instead of opening a window
import matplotlib.pyplot as plt  # noqa: E402

# ---- Settings you can change -------------------------------------------
CITY = "San Jose"
LATITUDE, LONGITUDE = 37.3382, -121.8863
DAYS_OF_HISTORY = 730          # about two years
# -------------------------------------------------------------------------

URL = "https://archive-api.open-meteo.com/v1/archive"
DAILY_VARIABLES = ["temperature_2m_max", "temperature_2m_min",
                   "precipitation_sum", "wind_speed_10m_max"]
COLUMN_NAMES = {"time": "date", "temperature_2m_max": "temp_high_f",
                "temperature_2m_min": "temp_low_f",
                "precipitation_sum": "precip_in",
                "wind_speed_10m_max": "wind_max_mph"}


def fetch_weather(latitude, longitude, start, end):
    """Ask the API for daily weather and return it as a DataFrame."""
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily": ",".join(DAILY_VARIABLES),
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "auto",
    }
    try:
        response = requests.get(URL, params=params, timeout=30)
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise SystemExit(f"Could not get data from the weather API: {exc}")

    if response.status_code != 200 or "daily" not in data:
        raise SystemExit(f"The weather API returned an error: "
                         f"{data.get('reason', response.status_code)}")

    df = pd.DataFrame(data["daily"]).rename(columns=COLUMN_NAMES)
    df["date"] = pd.to_datetime(df["date"])
    # The newest day or two can still be empty, so drop rows with no temperature
    return df.dropna(subset=["temp_high_f", "temp_low_f"]).reset_index(drop=True)


def summarize(df):
    """Print the highlights and return a month-by-month table."""
    hottest = df.loc[df["temp_high_f"].idxmax()]
    coldest = df.loc[df["temp_low_f"].idxmin()]
    rainy_days = int((df["precip_in"] >= 0.01).sum())

    print(f"\n{CITY}: {df['date'].min():%b %d, %Y} to {df['date'].max():%b %d, %Y} "
          f"({len(df)} days)")
    print(f"Hottest day:  {hottest['date']:%b %d, %Y} at {hottest['temp_high_f']:.1f} F")
    print(f"Coldest night: {coldest['date']:%b %d, %Y} at {coldest['temp_low_f']:.1f} F")
    print(f"Rainy days:   {rainy_days} ({rainy_days / len(df) * 100:.1f}% of days)")
    print(f"Total rain:   {df['precip_in'].sum():.1f} inches")

    monthly = df.groupby(df["date"].dt.to_period("M")).agg(
        avg_high_f=("temp_high_f", "mean"),
        avg_low_f=("temp_low_f", "mean"),
        rain_in=("precip_in", "sum")).round(1)
    return monthly


def make_charts(df, monthly):
    """Save a temperature trend chart and a monthly rainfall chart."""
    # Chart 1: daily highs and lows, plus a 30-day average of the highs
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["date"], df["temp_high_f"], color="#e8743b", alpha=0.35, label="Daily high")
    ax.plot(df["date"], df["temp_low_f"], color="#2a6fdb", alpha=0.35, label="Daily low")
    ax.plot(df["date"], df["temp_high_f"].rolling(30, min_periods=10).mean(),
            color="#c0392b", linewidth=2.5, label="30-day average high")
    ax.set_title(f"{CITY}: Daily Temperatures", fontsize=14, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (F)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("weather_temperature.png", dpi=150)
    plt.close(fig)

    # Chart 2: total rainfall per month
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = monthly.index.astype(str)
    ax.bar(labels, monthly["rain_in"], color="#2a6fdb")
    ax.set_title(f"{CITY}: Monthly Rainfall", fontsize=14, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel("Rain (inches)")
    ax.set_xticks(range(0, len(labels), 2))
    ax.set_xticklabels(labels[::2], rotation=45, ha="right")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig("weather_rainfall.png", dpi=150)
    plt.close(fig)


def main():
    # The archive runs about a week behind, so stop a week before today
    end = date.today() - timedelta(days=7)
    start = end - timedelta(days=DAYS_OF_HISTORY)

    df = fetch_weather(LATITUDE, LONGITUDE, start, end)
    df.to_csv("weather_data.csv", index=False)
    print(f"Saved {len(df)} days of data to weather_data.csv")

    monthly = summarize(df)
    make_charts(df, monthly)
    print("\nSaved weather_temperature.png and weather_rainfall.png")


if __name__ == "__main__":
    main()
