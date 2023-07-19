import requests
from flight_data import FlightData
from pprint import pprint

flight_Key = 'tequila api key'  # tequila api key
local_ep = 'https://tequila-api.kiwi.com/locations/query'  # location api endpoint
search_ep = 'https://tequila-api.kiwi.com/v2/search?'  # search api endpoint

class FlightSearch:
    #class used to interact with flight search api
    def __init__(self):
        self.destination_data = {}
        self.local_header = {
            'apikey': flight_Key,
            }
        self.local_params = {
        'locale': 'en-US',
        'location_types': 'airport',
        'limit': '1'
        }

        self.flight_params = {  # edit these params to interact as needed with the tequila api
            # 'locale': 'en',
            'curr': 'GBP',
            'flight_type': 'round',
            'nights_in_dst_from': 5,
            'nights_in_dst_to': 21,
            'max_stopovers': 0,
            'one_for_city': 1  # limits results to single cheapest option
        }

    def get_destination_code(self, city_name):
        self.local_params['term'] = city_name
        # print(self.local_params)
        response = requests.get(url=local_ep, params=self.local_params, headers=self.local_header)
        data = response.json()
        locations = data['locations']
        city_code = locations[0]['city']['code']
        return city_code

    def search_flights(self, origin_city, city_code, from_time, to_time):
        self.route = []
        self.stopovers = 0
        self.dest_city = ''
        self.flight_params['max_stopovers'] = 0
        self.flight_params['fly_from'] = origin_city
        self.flight_params['fly_to'] = city_code
        self.flight_params['date_from'] = from_time
        self.flight_params['date_to'] = to_time
        # self.flight_params['price_to'] = 1000
        print(self.flight_params)
        response = requests.get(url=search_ep, params=self.flight_params, headers=self.local_header)
        try:
            data = response.json()["data"][0]
            # pprint(response.json())
        except IndexError:
            print(f"No direct flights found for {city_code}.")
            try:
                self.flight_params['max_stopovers'] = 1
                response = requests.get(url=search_ep, params=self.flight_params, headers=self.local_header)
                data = response.json()["data"][0]
                print(f"Flights found for {city_code} with 1 stop over.")
                # pprint(response.json())
            except IndexError:
                print(f"No direct flights found for {city_code} with 1 stop over.")
                try:
                    self.flight_params['max_stopovers'] = 2
                    response = requests.get(url=search_ep, params=self.flight_params, headers=self.local_header)
                    data = response.json()["data"][0]
                    print(f"Flights found for {city_code} with 2 stop over.")
                    # pprint(response.json())
                except IndexError:
                    print(f"No direct flights found for {city_code} with 2 stop over.")
                    return None




        # pprint(data)
        # print(data['price'])

        for flight in data["route"]:
            self.route.append(flight['cityFrom'])
            if flight['cityCodeTo'] == city_code:
                self.dest_city = flight['cityTo']
        self.route.append(self.route[0])
        self.stopovers = self.flight_params['max_stopovers']

        flight_data = FlightData(
            price=data["price"],
            origin_city=self.route[0],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=self.dest_city,
            destination_airport=city_code,
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0],
            route=self.route,
            num_stops=self.stopovers
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        print(f'Flight route: {self.route}')
        return flight_data


