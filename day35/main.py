import json
import requests
import smtplib
import os
import datetime as dt
from zoneinfo import ZoneInfo


owm_api = "https://api.openweathermap.org/data/2.5/forecast"
owm_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
MY_LAT = 52.864529
MY_LONG = 17.948481
TIMEZONE = "Europe/Warsaw"
KELVIN_ZERO = -273.15
my_email = os.getenv("MY_EMAIL")
app_password = os.getenv("APP_PASSWORD")
recipient_email = os.getenv("RECIPIENT_EMAIL")


def get_forecast():
    parameters = {
        "lat": MY_LAT,
        "lon": MY_LONG,
        "appid": owm_api_key,
        "cnt": 4
    }
    response = requests.get(owm_api, params=parameters)
    response.raise_for_status()
    data = response.json()

    next_12_hours_forecast = {}
    for hour_forecast in data["list"]:
        date = hour_forecast["dt_txt"]
        dt_utc = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        dt_utc = dt_utc.replace(tzinfo=ZoneInfo("UTC"))
        dt_warsaw = dt_utc.astimezone(ZoneInfo("Europe/Warsaw"))
        time = dt_warsaw.strftime("%H:%M:%S")

        forecast = {
            "temperature": str(round(hour_forecast["main"]["temp"] + KELVIN_ZERO, 1)) + "*C",
            "perceived temperature": str(round(hour_forecast["main"]["feels_like"] + KELVIN_ZERO, 1)) + "*C",
            "humidity": str(hour_forecast["main"]["humidity"]) + "%",
            "pressure": str(hour_forecast["main"]["grnd_level"]) + "hPa",
            "wind speed": str(hour_forecast["wind"]["speed"]) + " m/s",
            "cloud cover": str(hour_forecast["clouds"]["all"]) + "%",
            "weather": hour_forecast["weather"][0]["description"]
        }
        next_12_hours_forecast[time] = forecast

    return next_12_hours_forecast


def send_email(forecast):

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        current_date = dt.datetime.now().strftime("%Y-%m-%d")
        connection.starttls()
        connection.login(user=my_email, password=app_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=recipient_email,
                            msg=f"Subject:Weather forecast for {current_date}\n\n{forecast}")
        

forecast = get_forecast()
forecast_formatted = json.dumps(forecast, indent=4)
send_email(forecast_formatted)
