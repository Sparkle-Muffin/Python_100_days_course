import os
import requests

class DataManager:
    def __init__(self):
        self.url = "https://api.sheety.co/4910a14988fdf9eb4b394f8d4634db0e/flightDeals/prices"


    def get_data(self):
        endpoint = self.url
        headers = {
            "Authorization": f"{os.getenv("SHEETY_BEARER_TOKEN")}"
            }
        response = requests.get(url=endpoint, headers=headers)
        data = response.json()
        sheet = data["prices"]
        return sheet


    def upload_iata_codes(self, sheet):
        headers = {
            "Authorization": f"{os.getenv("SHEETY_BEARER_TOKEN")}"
            }
        for i, row in enumerate(sheet):
            endpoint = f"{self.url}/{i+2}"
            parameters = {
                "price": row
            }
            response = requests.put(url=endpoint, headers=headers,json=parameters)
            print(response.text)
            