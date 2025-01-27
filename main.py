from data_manager import DataManager
from pprint import pprint
import requests
import os


google_sheets = DataManager()

sheets_data = google_sheets.get_data(None)

for item in sheets_data["sheet1"]:
    item["iata"] = "TESTING"


for item in sheets_data["sheet1"]:
    put_data = {
        "sheet1": {
            "iata": item["iata"],
        }
    }
    # print(put_data)
    print(item["id"])
    google_sheets.put_data(object_id=item["id"], put_data=put_data)

