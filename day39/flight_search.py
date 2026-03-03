import os
import requests
import datetime as dt


class FlightSearch:
    def __init__(self, origin_iata):
        self.api_key = os.getenv("AMADEUS_API_KEY")
        self.api_secret = os.getenv("AMADEUS_API_SECRET")
        self.origin_iata = origin_iata
        self.url = "https://test.api.amadeus.com/v1"


    def _get_access_token(self):
        endpoint = f"{self.url}/security/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        parameters = {
            "grant_type": "client_credentials",
            "client_id": f"{self.api_key}",
            "client_secret": f"{self.api_secret}"
        }
        response = requests.post(url=endpoint, headers=headers, data=parameters)
        data = response.json()
        self.token = data["access_token"]


    def get_iata_codes(self, sheet):
        self._get_access_token()
        endpoint = f"{self.url}/reference-data/locations/cities"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        new_sheet = []
        for row in sheet:
            city = row["city"].upper()
            parameters = {
                "keyword": f"{city}",
                "max": 1,
                "include": "AIRPORTS"
            }
            response = requests.get(url=endpoint, headers=headers, params=parameters)
            data = response.json()
            iata_code = data["data"][0]["iataCode"]
            row["iataCode"] = iata_code
            new_sheet.append(row)
        return new_sheet
    

    def get_flights_data(self, sheet):
        self._get_access_token()
        endpoint = f"{self.url}/shopping/flight-dates"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        tomorrow = dt.datetime.now().strftime("%Y-%m-%d")
        half_year_later = (dt.datetime.now() + dt.timedelta(days=183)).strftime("%Y-%m-%d")
        flights_data = []
        for row in sheet:
            # parameters = {
            #     "origin": f"{self.origin_iata}",
            #     "destination": f"{row["iataCode"]}",
            #     "departureDate": f"{tomorrow},{half_year_later}",
            #     "oneWay": "False",
            #     "maxPrice": f"{row["lowestPrice"]}"
            # }
            # response = requests.get(url=endpoint, headers=headers, params=parameters)
            parameters = {
                "origin": "PAR",
                "destination": "LON"
            }
            response = requests.get(url=endpoint, headers=headers, params=parameters)
            data = response.json()
            for flight in data["data"]:
                f_data = {
                    "price": f"{flight["price"]["total"]}",
                    "origin":  f"{flight["origin"]}",
                    "destination":  f"{flight["destination"]}"
                }
                flights_data.append(f_data)
            print(response.text)
            print(data)
        print(flights_data)
