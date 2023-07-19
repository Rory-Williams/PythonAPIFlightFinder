import requests
from pprint import pprint

sheety_ep = 'sheety endpoint'  # google sheet sheety api endpoint

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        # used to get initial stored data
        response = requests.get(url=sheety_ep)
        data = response.json()
        # print(f'data: {data}')
        self.destination_data = data["prices"]
        pprint(self.destination_data)
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{sheety_ep}/{city['id']}",
                json=new_data
            )
            # print(response.text)

    def update_destination_costs(self, price, id):
        new_data = {
            "price": {
                "lowestPrice": price
            }
        }
        response = requests.put(
            url=f"{sheety_ep}/{id}",
            json=new_data
        )
        print(f'response: {response.text}')
