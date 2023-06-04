from urllib.request import urlopen
import json
from datetime import datetime, timedelta

import pandas as pd

from location import Location
from setting import API_KEY

class Weather:
    def __init__(self, day = 0, clock = False):
        self.day = day
        self.clock = clock
        self.json_weather = None
        self.description = None
        self.temp = None
        self.humidity = None
        self.wind_speed = None
        self.time = None

        self.get_json_weather()

    def get_json_weather(self):
        loc = Location()
        if self.day == 0 and self.clock == False:
            WEATHER_DAY = f"https://api.openweathermap.org/data/2.5/weather?lat={loc.get_lat()}&lon={loc.get_lon()}&appid={API_KEY}&units=metric"
            self.json_weather = json.load(urlopen(WEATHER_DAY))
        elif self.clock == True:
            WEATHER_FEW_DAYS = f"https://api.openweathermap.org/data/2.5/forecast?lat={loc.get_lat()}&lon={loc.get_lon()}&appid={API_KEY}&units=metric"
            self.json_weather = json.load(urlopen(WEATHER_FEW_DAYS))

    def get_parse_weather(self, json_weather):
        self.description = json_weather['weather'][0]['description']
        self.temp = json_weather["main"]["temp"]
        self.humidity = json_weather["main"]["humidity"]
        self.wind_speed = json_weather["wind"]["speed"]
        if self.clock == True:
            self.time = json_weather["dt_txt"]

    def get_day(self):
        return self.day

    def get_weather(self):
        if self.clock == False:
            self.get_parse_weather(self.json_weather)
            return "Погода на данный момент в вашем городе:\n" \
                   f"Температура: {self.temp}°C\n" \
                   f"Погода: {self.description}\n" \
                   f"Влажность: {self.humidity}%\n" \
                   f"Скорость ветра: {self.wind_speed}м/с"

        day_gap = datetime.today() + timedelta(days=self.day)
        df = pd.DataFrame(columns=["Температура", "Погода", "Время"])
        for i in range(len(self.json_weather["list"])):
            self.get_parse_weather(self.json_weather["list"][i])
            date = datetime.strptime(self.time, "%Y-%m-%d %H:%M:%S")
            if (day_gap.date() - date.date()).days >= 0:
                df.loc[i] = [self.temp, self.description, self.time]

        return df
