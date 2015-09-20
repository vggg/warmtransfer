'''
Configuration Settings
'''

''' Uncomment to configure using the file.  
WARNING: Be careful not to post your account credentials on GitHub.

TWILIO_ACCOUNT_SID = "ACCT_SID"
TWILIO_AUTH_TOKEN = "A_TOKEN"
TWILIO_CALLER_ID = "Tel Id"
'''

import os
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', None)
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', None)
TWILIO_CALLER_ID = os.environ.get('TWILIO_CALLER_ID', None)
TWILIO_APP_SID = os.environ.get('TWILIO_APP_SID', None)
