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
def event_list(request):
    user = request.session['user']
    if user['role'] != "host":
        redirect("/login")

    host = Host.objects.get(person_id=user["id"])
    events = Event.objects.filter(host_id=host, status=0)

    bids = dict()
    for event in events:
        bids[event.id] = Bid.objects.filter(event=event, status__in=[0, 3, 5])

    booking_events = Event.objects.filter(status=1)
    
    bookings = dict()
    for event in booking_events:
    	try:
	        bk = Booking.objects.filter(event=event)[0]
	        bookings[event.id] = [bk, bk.bid.dj.title, bk.status]
        except:
        	pass

    return render_to_response('events/list.html', locals(), context_instance=RequestContext(request))

@login_required()
def event_create(request):
	user = request.session['user']

	genre = settings.GENRE
	event_type = settings.EVENT_TYPE
	rate = settings.PRICE

	if user['role'] != "host":
		return redirect("/login")
	else:
		country_name = settings.COUNTRY
		types = settings.EVENT_TYPE

		if request.POST:
			user = Host.objects.filter(person_id=user["id"])[0]
			
			address = Address()
			address.street = request.POST["address"]
			address.city = request.POST["city"]
			address.state = request.POST["state"]
			address.country = request.POST["country"]
			address.zip_code = request.POST["zipcode"]
			address.lat = float(request.POST["lat"])
			address.lng = float(request.POST["lng"])
			address.save()

			event = Event()
			event.title = request.POST['title']
			event.description = request.POST['description']
			event.address = address
			event.genre = ','.join(request.POST.getlist('genre'))
			event.event_type = ','.join(request.POST.getlist('event_type'))

			date = request.POST["date"].split("/")
			str_date = "%s-%s-%s" % (date[2], date[0], date[1])
			event.date = str_date

			event.start_time = "%s-%s-%s %s:00" % (date[2], date[0], date[1], request.POST['start_time'])
			event.end_time = "%s-%s-%s %s:00" % (date[2], date[0], date[1], request.POST['end_time'])
			event.price = request.POST['price']
			event.type = "" #request.POST['event_type']
			event.host = user
			event.status = 0
			event.save()

			return redirect("/events/list")

		return render_to_response('events/create.html', locals(), context_instance=RequestContext(request))

@login_required()
def event_detail(request):
	user = request.session['user']

	if user['role'] != "host":
		return redirect("/login")

	if 'cancel_offer' in request.GET:
		booking_id = request.GET['booking_id']

		booking = Booking.objects.get(pk=booking_id)
		event = booking.event

		booking.bid.status = 0
		booking.bid.save()

		booking.bid.event.status = 0
		booking.bid.event.save()

		booking.delete()


	else:
		id = request.GET['id']
		event = Event.objects.get(pk=id)
		stripe_pk = settings.STRIPE_PUBLIC_KEY

	bids = Bid.objects.filter(event=event).exclude(status=1)
	bookings = Booking.objects.filter(event=event, status__lt=2)

	return render_to_response('events/detail.html', locals(), context_instance=RequestContext(request))

@login_required()
def remove_event(request):
	id = request.GET['id']
	event = Event.objects.get(pk=id)

	bookings = Booking.objects.filter(event=event, status__lt=2)
	if len(bookings) > 0:
		return redirect("/events/list")

	event.status = 3
	event.save()

	bids = Bid.objects.filter(event=event, status__in=[0, 3])
	for bid in bids:
		bid.status = 1
		bid.message = "Cancel Event."
		bid.save()

		nf = Notification()
		nf.sender = bid.event.host.id
		nf.receiver = bid.dj.person
		nf.content = "Proposal Ended: %s. Reason: Cancel job." % (bid.event.title)
		nf.url = ""
		nf.save()

	return redirect("/events/list")
