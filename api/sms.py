# works with both python 2 and 3
from __future__ import print_function

import africastalking
import os

class SMS:
    def __init__(self):
        # Set your app credentials
        self.username = os.environ.get('SMS_API_USERNAME', None)
        self.api_key = os.environ.get('SMS_API_KEY', None)

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, recepients, item):
        # Set your message
        message = "Your order for {} has been received".format(item);
        # Set your shortCode or senderId
        sender = os.environ.get('SHORTCODE', None)
        try:
            # Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(message, recepients)
            print (response)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))
