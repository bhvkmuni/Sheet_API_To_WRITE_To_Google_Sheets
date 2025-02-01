import os
import requests
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"



class FlightSearch:

    def __init__(self):
        self._api_key = os.getenv("FLIGHT_API")
        self._api_secret = os.getenv("FLIGHT_SECRET")
        self._token = self._get_new_token()
        self.flight_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"


    def _get_new_token(self):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret,
        }
        response = requests.post(url=TOKEN_ENDPOINT, headers=headers, data=data)
        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def get_iata_code(self, city):
        headers = {
            "Authorization": f"Bearer {self._token}"
        }

        response = requests.get(url=f"{IATA_ENDPOINT}?keyword={city}&max=1", headers=headers)
        try:
            code = response.json()["data"][0]["iataCode"]
        except IndexError:
            print(f"IndexError: No airpot code found for {city}.")
            return "N/A"
        except KeyError:
            print(f"KeyError: No airport cod found for {city}.")
            return "Not Found"
        return code


    def flight_search(self, origin_city_code, destination_city_code, from_time, to_time):
        header = {
            "Authorization": f"Bearer {self._token}"
        }
        response = requests.get(
            url=f"{self.flight_endpoint}?"
                f"originLocationCode={origin_city_code}&"
                f"destinationLocationCode={destination_city_code}&"
                f"departureDate={from_time.strftime("%Y-%m-%d")}&"
                f"returnDate={to_time.strftime("%Y-%m-%d")}&" 
                f"adults=1&"
                f"nonStop=true&"
                f"currencyCode=USD&"
                f"max=2",
            headers=header
        )
        return response.json()






