import twilio
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()


account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_AUTH"]
client = Client(account_sid, auth_token)



class NotificationManager:

    def __init__(self, price, depart_code, arrival_code, outbound_date, inbound_date):
        self.price = price
        self.depart_code = depart_code
        self.arrival_code = arrival_code
        self.outbound_date = outbound_date
        self.inbound_date = inbound_date


    def sms_trigger(self):
        message = client.messages.create(
            body=f"Low price alert! Only USD{self.price} to "
                 f"fly from {self.depart_code} to "
                 f"{self.arrival_code} on {self.outbound_date}"
                 f"{self.inbound_date}.",
            from_="+18312310463",
            to="+918657152191",
        )
        print(message.body)

