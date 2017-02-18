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
from allauth.socialaccount.models import SocialAccount

from djeer_auth.views import login_required

# @login_required()
def help_edit(request):
    user = request.session['user']

    return render_to_response('help/edit.html', locals(), context_instance=RequestContext(request))

def help_live(request):
    if 'user' in request.session:
        user = request.session['user']
    else:
        user = None

    help = Help.objects.filter(title__iexact="How it works")[0]
    if "key" in request.GET:
        temp = Help.objects.filter(title__iexact=request.GET["key"])
        if len(temp) > 0:
            help = temp[0]

    res = []
    top_levels = Help.objects.filter(parent=None).order_by("sort")
    for tp in top_levels:
        temp = {"top": tp}

        temp["children"] = Help.objects.filter(parent=tp).order_by("sort")
        temp["active"] = ""
        if tp.id == help.id or help.id in [item.id for item in temp["children"]]:
            temp["active"] = "active"

        res.append(temp)

    return render_to_response('help/live.html', locals(), context_instance=RequestContext(request))

