from weather_api_caller import Weather_API_caller
from datetime import datetime, timedelta
import functions_framework
from google.cloud import storage
import pandas as pd
import argparse
import logging
import json
from error_notifier import error_notifier

EMAIL_RECIPIENT="alvaro.larraya1@gmail.com"

@error_notifier(EMAIL_RECIPIENT, EMAIL_PASSWORD)
@functions_framework.http
def daily_call(request):
    yesterday = datetime.now() - timedelta(days=1)

    START_DATE = yesterday.strftime("%Y-%m-%d") 
    END_DATE = datetime.now() + timedelta(days=1)
    BUCKET_NAME = "api_results"

    logger = logging.getLogger("weather-caller")

    date_range = pd.date_range(start=START_DATE, end=END_DATE)
    dates = [d.strftime("%Y-%m-%d") for d in date_range]

    api_caller = Weather_API_caller(API_KEY,logger)
    for date in dates:
        daily_aggregation_weather = api_caller.get_daily_aggregation_data(date=date)
        # print(json.dumps(daily_aggregation_weather, indent=4))
        filename = date+".jsonl"
        with open("responses/"+filename, "w", encoding="utf-8") as f:
            if isinstance(daily_aggregation_weather, list):
                for obj in daily_aggregation_weather:
                    f.write(json.dumps(obj) + "\n")
            else:
                f.write(json.dumps(daily_aggregation_weather) + "\n")
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_filename("responses/"+filename)
        os.remove("responses/"+filename)
    return "daily aggregation weather data ingested succesfully"