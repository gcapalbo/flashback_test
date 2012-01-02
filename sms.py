from urllib import urlencode
from urllib2 import urlopen
from django.conf import settings

def send_sms(numberToDial, msg):
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
