from urllib import urlencode
from urllib2 import urlopen
from django.conf import settings
from twilio.rest import TwilioRestClient
from .models import log

def send_sms_tropo(numberToDial, msg):
    params = urlencode({
        "action"        : "create"
       ,"token"         : getattr(settings, "FLASHBACK_TEST_TROPO_MESSAGING_TOKEN")
       ,"numberToDial"  : numberToDial
       ,"msg"           : msg
       ,"_send_sms"     : "true"
    })
    url = "https://api.tropo.com/1.0/sessions?%s" % params
    response = urlopen(url).read()
    print response

def send_sms_twilio(numberToDial, msg):
    sid = getattr(settings, "TWILIO_ACCOUNT_SID")
    token = getattr(settings, "TWILIO_AUTH_TOKEN")
    source_number = getattr(settings, "TWILIO_NUMBER")
    client = TwilioRestClient(sid, token)
    message = client.sms.messages.create(to=numberToDial,from_=source_number,body=msg)
    log("OUT", "TEXT", numberToDial, "TWILIO", None, message=msg)


