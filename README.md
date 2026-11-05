# Weather Data Project: San Jose vs. Seattle
 
A Python script that collects two years of daily weather for two cities from a public API,
saves it to CSV, and compares the cities with a summary table and charts.
 
## What it does
- Pulls daily high and low temperature, rainfall, and wind speed from the free
  [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
- Combines both cities into one dataset (`weather_data.csv`, 1,462 rows)
- Builds a side-by-side comparison table (`city_comparison.csv`)
- Charts 30-day average temperatures and monthly rainfall for both cities
- Handles API errors and the archive's few-day delay
## Results (Oct 2024 - Oct 2026, 731 days per city)
 
| | San Jose, CA | Seattle, WA |
|---|---|---|
| Average high (F) | 72.7 | 60.6 |
| Average low (F) | 51.8 | 47.9 |
| Hottest day (F) | 100.8 | 91.7 |
| Coldest night (F) | 29.8 | 24.1 |
| Rainy days (%) | 19.8 | 41.7 |
| Total rain (in) | 41.4 | 82.1 |
| Average max wind (mph) | 7.8 | 10.5 |
 
**Takeaways**
- San Jose's average daily high is 12.1 F warmer than Seattle's.
- Seattle gets about twice the rainfall and rains on more than twice as many days.
- San Jose has a bigger day-to-night swing (about 21 F between the average high and low,
  versus about 13 F in Seattle).
- Seattle is windier on average and had the colder coldest night.
<img src="weather_temperature.png" width="700" alt="Temperature comparison">
<img src="weather_rainfall.png" width="700" alt="Monthly rainfall comparison">
## How to run
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python weather_project.py
```
The script saves the data, the comparison table, and both charts in the same folder.
 
## Compare different cities
Edit the `CITIES` list at the top of `weather_project.py`. Each entry is a name with its
latitude and longitude, for example `"Phoenix": (33.4484, -112.0740)`.
 
## Tools
Python, requests, pandas, matplotlib
 
## Data
Weather data by [Open-Meteo.com](https://open-meteo.com/) (CC BY 4.0).