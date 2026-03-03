import requests
import os
import datetime as dt

python_100_days_endpoint = "https://app.100daysofpython.dev/v1/nutrition/natural/exercise"
sheety_endpoint = "https://api.sheety.co/4910a14988fdf9eb4b394f8d4634db0e/workoutTracking/workouts"


########################################################################
##                      GET SPORT ACTIVITY INFO                       ##
########################################################################

headers = {
    "Content-Type": "application/json",
    "x-app-id": os.getenv("PYTHON100DAYS_APP_ID"),
    "x-app-key": os.getenv("PYTHON100DAYS_API_KEY")
}

user_iput = input("Describe your sport activity: ")
# user_iput = "run for 10 miles"

parameters = {
    "query": f"{user_iput}",
    "weight_kg": 75,
    "height_cm": 178,
    "age": 30,
    "gender": "male"
}

response = requests.post(url=python_100_days_endpoint, headers=headers, json=parameters)
result = response.json()
data = result["exercises"][0]
exercise = data["name"].title()
duration = data["duration_min"]
calories = data["nf_calories"]

print(result["exercises"][0])


########################################################################
##                    UPLOAD DATA TO GOOGLE SHEETS                    ##
########################################################################

now = dt.datetime.now()
date = now.strftime("%d/%m/%Y")
time = now.strftime("%H:%M:%S")

headers = {"Authorization": f"{os.getenv("SHEETY_BEARER_TOKEN")}"}

parameters = {
    "workout": {
        "date": f"{date}",
        "time": f"{time}",
        "exercise": f"{exercise}",
        "duration": f"{duration}",
        "calories": f"{calories}",
    }
}

response = requests.post(url=sheety_endpoint, headers=headers, json=parameters)
print(response.text)
