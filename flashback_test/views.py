import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from tropo import Tropo
from twilio import twiml
from .forms import SendMessageForm
from .models import log
from .sms import send_sms_tropo, send_sms_twilio

"""
This is the view that will be invoked by a tropo WebAPI application.
"""
@csrf_exempt
def tropo_view(request):
    if request.method == "POST":
        data = json.loads(request.raw_post_data)
        session = data["session"]
        if "parameters" in session:
            params = session["parameters"]
            if ("_send_sms" in params) and ("numberToDial" in params) and ("msg" in params):
                numberToDial = params["numberToDial"]
                msg = params["msg"]
                t = Tropo()
                t.call(to = numberToDial, network = "SMS")
                t.say(msg)
                log("OUT", "TEXT", numberToDial, "TROPO", request.raw_post_data, msg)
                return HttpResponse(t.RenderJson())
        if "from" in session:
            caller_id = session["from"]["id"]
            channel = session["from"]["channel"]
            msg = None
            if "initialText" in session:
                msg = session["initialText"]
            log("IN", channel, caller_id, "TROPO", request.raw_post_data, msg)
            if channel == "VOICE":
                send_sms(caller_id, "Callback received.")
        t = Tropo()
        t.hangup()
        return HttpResponse(t.RenderJson())
    else:
        return HttpResponseBadRequest()

"""
This is the view that will be invoked by Twilio.
"""
@csrf_exempt
def twilio_view(request):
    if request.method == "POST":
        caller_id = None
        try:
            caller_id = request.POST["From"]
        except Exception as e:
            pass
        r = twiml.Response()
        r.reject()
        log("IN", "VOICE", caller_id, "TWILIO", request.raw_post_data)
        return HttpResponse(str(r))
    else:
        return HttpResponseBadRequest()

"""
This view is used to kick off the test by sending
the tester a text message.
"""
@login_required
def send_message(request):
    if request.method == "POST":
        form = SendMessageForm(request.POST)
        if form.is_valid():
            numberToDial = form.cleaned_data["mobile_number"]
            msg = form.cleaned_data["message"]
            backend = form.cleaned_data["backend"]
            if backend == "TROPO":
                send_sms_tropo(numberToDial, msg)
            elif backend == "TWILIO":
                send_sms_twilio(numberToDial, msg)
    else:
        form = SendMessageForm()
    return render(request, "send_message.html", {"form" : form})

