# works with both python 2 and 3
from __future__ import print_function

import africastalking
import os

class SMS:
    def __init__(self):
        # Set your app credentials
        self.username = "sandbox"
        self.api_key = os.environ.get('SMS_API_KEY', None)

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, recepients, id):
        # Set the numbers you want to send to in international format
        #recipients = ["+254713YYYZZZ", "+254733YYYZZZ"]

        # Set your message
        message = "Your order code name {} has been received".format(id);
        # Set your shortCode or senderId
        sender = os.environ.get('SHORTCODE', None)
        try:
            # Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(message, recepients, sender)
            print (response)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))
