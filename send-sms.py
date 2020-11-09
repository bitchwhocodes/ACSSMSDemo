import os
from azure.communication.sms import PhoneNumber
from azure.communication.sms import SendSmsOptions
from azure.communication.sms import SmsClient
connection_string =  '<PUT YOUR CONNECTION STRING HERE>'
sms_client = SmsClient.from_connection_string(connection_string)


try:
    # Quickstart code goes here
# calling send() with sms values
        sms_response = sms_client.send(
                from_phone_number=PhoneNumber("+18330001122"),
                to_phone_numbers=[PhoneNumber("+17201112233")],
                message="Hello World via SMS",
                send_sms_options=SendSmsOptions(enable_delivery_report=True)) # optional property
except Exception as ex:
    print('Exception:')
    print(ex)
