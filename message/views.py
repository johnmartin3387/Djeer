from django.shortcuts import render_to_response, redirect
from djeer_auth.models import *
from django.template import RequestContext
from django.contrib.auth.models import *
from djeer import settings

from django.http import HttpResponse
from functools import wraps

import datetime
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from djeer_auth.views import login_required

@login_required()
def message_request(request):
    user = request.session["user"]

    message = "1"
    target = ""
    if "dialog" in request.GET:
        target = request.GET["dialog"]

    return render_to_response('message/message.html', locals(), context_instance=RequestContext(request))

@login_required()
def notification(request):
    user = request.session["user"]

    res = dict()
    notification = Notification.objects.filter(receiver_id=int(user["id"]), status=0)
    res['count'] = len(notification)

    res['content'] = []
    for nf in notification:
    	res['content'].append({"message": nf.content, "url": nf.url})

    return HttpResponse(json.dumps(res)) 

@login_required()
def reset_notification(request):
    user = request.session["user"]

    res = dict()
    notification = Notification.objects.filter(receiver_id=int(user["id"]), status=0)
    
    for nf in notification:
    	nf.status = 1
    	nf.save()

	res = dict()
    notification = Notification.objects.filter(receiver_id=int(user["id"]), status=0)
    res['count'] = len(notification)

    return HttpResponse(json.dumps(res))
