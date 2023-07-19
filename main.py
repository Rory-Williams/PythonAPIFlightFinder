from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import FlightData
from datetime import datetime, timedelta
import requests

# flight search script to check for lowest cost flights to various airports from a given airport over given time frame
# edit params in flight search to edit search options with tequila api
# require google sheets sheety access and endpoint for included excel sheet
# requires tequila api key


# sheety_ep = 'https://api.sheety.co/6c54c17eb15271b87094446e0225e552/flightDeals/prices'
# flight_Key = 'X6MivaGQ_JrhhpLbiQKAaq0xgF3nXTxn'
#
# sheet_res = requests.get(url=sheety_ep)
# sheet_res = sheet_res.json()
# print(sheet_res)

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

flight_search = FlightSearch()
if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        print(row)
        print(row['city'])
        row["iataCode"] = flight_search.get_destination_code(row["city"])  # gets the iata airport code for city in spreadsheet
    print(f"sheet_data:\n {sheet_data}")
    data_manager.update_destination_codes()

# self.today = datetime.today()
# self.future = timedelta(weeks=24)
# self.future = self.today + self.future
# self.future = self.future.strftime('%d/%m/%Y')
# self.today = self.today.strftime('%d/%m/%Y')
tomorrow = datetime.now() + timedelta(days=1)
tomorrow = tomorrow.strftime('%d/%m/%Y')
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
six_month_from_today = six_month_from_today.strftime('%d/%m/%Y')

ORIGIN_CITY_IATA = "LON"
for row in sheet_data:
    flight = flight_search.search_flights(
        ORIGIN_CITY_IATA,
        row["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    try:
        data_manager.update_destination_costs(flight.price,row['id'])
    except AttributeError:
        print(f'No flights found for {row["city"]}')










