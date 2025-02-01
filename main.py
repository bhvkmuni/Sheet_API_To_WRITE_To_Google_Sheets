from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from flight_data import FlightData, find_cheapest_flight
import time
from notification_manager import NotificationManager


from pprint import pprint
import requests
import os

google_sheets = DataManager()
flights_ama = FlightSearch()
sheets_data = google_sheets.get_data()


#ORIGIN AIRPORT
ORIGIN_CITY_IATA = "BOM"


# ============================= Update the Airport Codes in Google Sheet ================

for row in sheets_data["sheet1"]:
    if row["iata"] == "":
        row["iata"] = flights_ama.get_iata_code(row["city"])
        time.sleep(2)
print(f"sheet_data:\n {sheets_data}")

google_sheets.destination_data = sheets_data
google_sheets.update_destination_codes()


# ================= Search for Flights ========================================
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6*30))


for destination in sheets_data["sheet1"]:
    print(f"Getting flights for {destination["city"]}.....")
    flights = flights_ama.flight_search(
        origin_city_code=ORIGIN_CITY_IATA,
        destination_city_code=destination["iata"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination["city"]}: USD{cheapest_flight.price}")
    if cheapest_flight.price !="N/A" and cheapest_flight.price < destination["price"]:
        print(f"Lower price flight to {destination["city"]}!")
        twilio = NotificationManager(price=cheapest_flight.price,
                                     depart_code=ORIGIN_CITY_IATA,
                                     arrival_code=destination["iata"],
                                     outbound_date=tomorrow,
                                     inbound_date=six_month_from_today)
        twilio.sms_trigger()
    time.sleep(2)
