from src.weather_api_caller import Weather_API_caller
from google.cloud import storage
from dotenv import load_dotenv
import pandas as pd
import argparse
import logging
import json

load_dotenv("secrets.env")
START_DATE = "2023-01-01"
END_DATE = "2025-03-29"
BUCKET_NAME = "api_results"

parser = argparse.ArgumentParser(description="Historical OpenWeather data ingestion")
parser.add_argument("--api_key", type=str, help="API key", default=None)
API_KEY = parser.parse_args().api_key
if(API_KEY is None):
    raise Exception("No OpenWeather API key found")

logger = logging.getLogger("weather-caller")

date_range = pd.date_range(start=START_DATE, end=END_DATE)
dates = [d.strftime("%Y-%m-%d") for d in date_range]

api_caller = Weather_API_caller(API_KEY,logger)
for date in dates:
    daily_aggregation_weather = api_caller.get_daily_aggregation_data(date=date)
    filename = date+".jsonl"
    with open("src/responses/"+filename, "w", encoding="utf-8") as f:
        if isinstance(daily_aggregation_weather, list):
            for obj in daily_aggregation_weather:
                f.write(json.dumps(obj) + "\n")
        else:
            f.write(json.dumps(daily_aggregation_weather) + "\n")
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_filename("src/responses/"+filename)