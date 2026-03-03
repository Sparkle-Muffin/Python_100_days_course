import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
import os
import smtplib


MY_LAT = 52.864529
MY_LONG = 17.948481
TIMEZONE = "Europe/Warsaw"
my_email = os.getenv("MY_EMAIL")
app_password = os.getenv("APP_PASSWORD")
recipient_email = os.getenv("RECIPIENT_EMAIL")

def get_ISS_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    return iss_latitude, iss_longitude

def get_sunrise_and_sunset():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
        "tzid": TIMEZONE
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = datetime.fromisoformat(data["results"]["sunrise"]).astimezone(ZoneInfo(TIMEZONE))
    sunset = datetime.fromisoformat(data["results"]["sunset"]).astimezone(ZoneInfo(TIMEZONE))
    return sunrise, sunset

def check_if_now_is_night():
    time_now = datetime.now().astimezone(ZoneInfo(TIMEZONE))
    sunrise, sunset = get_sunrise_and_sunset()
    time_buffer = timedelta(minutes=30)

    if time_now < sunrise + time_buffer or time_now > sunset - time_buffer:
        return True
    else:
        return False

def check_if_ISS_is_close():
    iss_latitude, iss_longitude = get_ISS_position()
    position_buffer = 5

    if abs(iss_latitude - MY_LAT) < position_buffer and abs(iss_longitude - MY_LONG) < position_buffer:
        return True
    else:
        return False

def send_email():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=app_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=recipient_email,
                            msg=f"Subject:ISS passing by!\n\nLook up, there is ISS somewhere above you!")

while True:
    if check_if_now_is_night() == True:
        if check_if_ISS_is_close() == True:
            send_email()
            pass
    time.sleep(60)
