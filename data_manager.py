from pprint import pprint
import requests
import os
from dotenv import load_dotenv

load_dotenv()

SHEETS_API = os.getenv("SHEETS_API")

class DataManager:
    def __init__(self):
        self.get_endpoint = "https://api.sheety.co/f54d34d24aad074c649e839b15a8a0ed/flightDeals/sheet1"
        self.post_endpoint = "https://api.sheety.co/f54d34d24aad074c649e839b15a8a0ed/flightDeals/sheet1"
        self.put_endpoint = "https://api.sheety.co/f54d34d24aad074c649e839b15a8a0ed/flightDeals/sheet1"
        self.sheets_headers = {
            "Authorization": f"Bearer {SHEETS_API}",
            "Content-Type": "application/json"
        }

        self.destination_data = {}


    def get_data(self):
        get_response = requests.get(url=self.get_endpoint, headers=self.sheets_headers)
        get_json_data = get_response.json()
        return get_json_data

    def put_data(self, object_id, put_data):
        put_response = requests.put(url=f"{self.put_endpoint}/{object_id}",
                                    headers=self.sheets_headers,
                                    json=put_data)
        print(put_response.text)

    def update_destination_codes(self):
        for city in self.destination_data["sheet1"]:
            new_data = {
                "sheet1": {
                    "iata": city["iata"]
                }
            }
            response = requests.put(
                url=f"{self.put_endpoint}/{city["id"]}",
                headers=self.sheets_headers,
                json=new_data
            )
            print(response.text)