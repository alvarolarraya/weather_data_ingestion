import requests
import json

class Weather_API_caller:

    def __init__(self,api_key,logger):
        self.api_key = api_key 
        self.logger = logger
        message = "Weather API caller initialized"
        print(message)
        self.logger.info(message)
        return
    
    def get_daily_aggregation_data(self,
                                   date:str,
                                   latitude:float=43.53573,
                                   longitude:float=-5.66152,
                                   units:str="metric") -> json:
        message = f'Daily aggregation request with date="{date}",latitude={latitude}'+\
                  f',longitude={longitude},units="{units}"'
        self.logger.info(message)
        print(message)
        daily_aggregation_url = "https://api.openweathermap.org/data/3.0/onecall/day_summary?"+\
                                    f"lat={latitude}&"+\
                                    f"lon={longitude}&"+\
                                    f"appid={self.api_key}&"+\
                                    f"units={units}&"+\
                                    f"date={date}"
        try:
            response = requests.get(daily_aggregation_url)
            if response.status_code != 200:
                message = "The OpenWeather API call failed with "+\
                         f"a {response.status_code} status code"
                self.logger.error(message)
                raise Exception(message)
        except Exception as e:
            # aplicar logger
            message = f"Something went wrong calling the OpenWeather API: {e}"
            self.logger.error(message)
            raise Exception(message)
        return response.json()