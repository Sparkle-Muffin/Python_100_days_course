# ACHTUNG!!!
# amadeus, kiwi and skyscanner do not work anymore for free.


from pathlib import Path
import json
BASE_DIR = Path(__file__).parent
test_sheet_path = BASE_DIR / "test_sheet.json"
with open(test_sheet_path) as file:
    test_sheet = json.load(file)


from flight_search import FlightSearch
from data_manager import DataManager

origin_iata = "LON"

# data_manager = DataManager()
flight_search = FlightSearch(origin_iata)

# 1) Fill IATA codes
# sheet = data_manager.get_data()
# sheet_with_codes = flight_search.get_iata_codes(sheet)
# data_manager.upload_iata_codes(sheet_with_codes)

# 2) Get data about flights
# sheet = data_manager.get_data()
flight_data = flight_search.get_flights_data(test_sheet["prices"])
