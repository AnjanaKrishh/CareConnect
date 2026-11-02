
import os
from twilio.rest import Client

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+910000000000",
    from_="+17372508034",
    body="sms_appointment_reminders",
)

print(message.sid)
