import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from tropo import Tropo
from .forms import SendMessageForm
from .models import log
from .sms import send_sms

"""
This is the view that will be invoked by a tropo WebAPI application.
"""
@csrf_exempt
def default(request):
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
                log("OUT", "TEXT", numberToDial, msg)
                return HttpResponse(t.RenderJson())
        if "from" in session:
            caller_id = session["from"]["id"]
            channel = session["from"]["channel"]
            msg = None
            if "initialText" in session:
                msg = session["initialText"]
            log("IN", channel, caller_id, msg)
            if channel == "VOICE":
                send_sms(caller_id, "Callback received.")
        t = Tropo()
        t.hangup()
        return HttpResponse(t.RenderJson())
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
            send_sms(numberToDial, msg)
    else:
        form = SendMessageForm()
    return render(request, "send_message.html", {"form" : form})

