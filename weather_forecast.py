import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from decimal import Decimal


class WeatherForecast:

    def __init__(self, api_key=None):
        self.JST = timezone(timedelta(hours=9), "JST")
        env = os.getenv("env", "local")
        if env == "local":
            load_dotenv(".env.local")
            self.api_key = os.getenv("api_key")
        else:
            self.api_key = api_key
        self.lat = os.getenv("lat")
        self.lon = os.getenv("lon")
        self.slack_web_hook_url = os.getenv("slack_web_hook_url")

    def get_weather_forecast(self, lat, lon):
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            return weather_data
        else:
            return None

    def edit_weather_forecast(self, weather_data):
        filtered_data = []
        for forecast in weather_data["list"]:
            forecast_date = datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S")
            forecast_date_plus_9_hours = self.conv_utc_to_jst(forecast_date)

            is_today = (
                forecast_date_plus_9_hours.date() == datetime.now(self.JST).date()
            )
            if is_today:
                filtered_data.append(
                    {
                        "date": forecast_date_plus_9_hours.date(),
                        "time": forecast_date_plus_9_hours.time().strftime("%H:%M")[:5],
                        "main": forecast["weather"][0]["main"],
                        "description": forecast["weather"][0]["description"],
                        "temp_min": forecast["main"]["temp_min"],
                        "temp_max": forecast["main"]["temp_max"],
                    }
                )
        return filtered_data

    def conv_utc_to_jst(self, utc_datetime):
        return utc_datetime + timedelta(hours=9)

    def edit_message(self, filtered_data):
        message = "\n".join(
            [
                f"日付：{data['date']} 時間：{data['time']} 天気：{data['main']} 詳細：{data['description']} 気温：{self.conv_celsius(data['temp_min'])} 〜 {self.conv_celsius(data['temp_max'])}"
                for data in filtered_data
            ]
        )
        if message == "":
            message = "今日の天気情報はありません"
        return message

    def conv_celsius(self, temp):
        result = Decimal(temp) - Decimal(273.16)
        return round(result, 1)

    def post_slack_message(self, message):
        url = f"https://hooks.slack.com/services{self.slack_web_hook_url}"
        data = {"text": message}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            print("Failed to post slack message")

    def get_dummy_weather_data(self):
        weather_data = {
            "list": [
                {
                    "dt": 1717275600,
                    "main": {
                        "temp": 290.48,
                        "feels_like": 290.33,
                        "temp_min": 290.47,
                        "temp_max": 290.48,
                        "pressure": 1009,
                    },
                    "weather": [
                        {
                            "id": 500,
                            "main": "Rain",
                            "description": "light rain",
                            "icon": "10d",
                        }
                    ],
                    "dt_txt": "2024-06-01 21:00:00",
                },
                {
                    "dt": 1717286400,
                    "main": {
                        "temp": 290.82,
                        "feels_like": 290.63,
                        "temp_min": 290.82,
                        "temp_max": 290.91,
                        "pressure": 1009,
                    },
                    "weather": [
                        {
                            "id": 500,
                            "main": "Rain",
                            "description": "light rain",
                            "icon": "10d",
                        }
                    ],
                    "dt_txt": "2024-06-01 21:00:00",
                },
            ]
        }
        return weather_data

    def main(self):
        print("Start weather forecast")
        weather_data = self.get_weather_forecast(self.lat, self.lon)
        if weather_data is None:
            self.post_slack_message("天気情報取得に失敗しました")
            return
        filtered_data = self.edit_weather_forecast(weather_data)
        message = self.edit_message(filtered_data)
        self.post_slack_message(message)
        print("End weather forecast")


if __name__ == "__main__":
    weather_forecast = WeatherForecast()
    weather_forecast.main()
