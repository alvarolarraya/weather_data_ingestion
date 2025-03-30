import pytest
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from weather_api_caller import Weather_API_caller

def test_daily_aggregation_call():
    DATE = "2025-03-27"
    LATITUDE=43.53573
    LONGITUDE=-5.66152
    UNITS="metric"
    api_caller = Weather_API_caller(API_KEY)
    daily_aggregation_weather = api_caller.get_daily_aggregation_data(date=DATE,\
                                latitude=LATITUDE,longitude=LONGITUDE,units=UNITS)
    
    with open("tests/daily_aggregation_correct_response.json", "r", encoding="utf-8") as f:
        daily_aggregation_correct_response = json.load(f)

    print("LLAMADA API",daily_aggregation_weather)
    print("JSON CORRECTO",daily_aggregation_correct_response)
    
    assert daily_aggregation_weather==daily_aggregation_correct_response