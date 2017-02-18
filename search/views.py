from django.shortcuts import render_to_response, redirect
from djeer_auth.models import *
from django.template import RequestContext
from django.contrib.auth.models import *
from djeer import settings

from django.http import HttpResponse
from functools import wraps

import datetime
import json
import urllib
import re

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from djeer_auth.views import login_required

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required()
def dashboard(request):
	user = request.session['user']

	menu = "dashboard"

	person = Person.objects.get(pk=user["id"])

	event_type = settings.EVENT_TYPE
	genre = settings.GENRE
	equipment = Equipment.objects.all()
	address = Address.objects.filter(city=person.address.city)
	neighborhoods = []
	for addr in address:
		nghb = Person.objects.filter(address=addr)
		if len(nghb) > 0:
			neighborhoods.append(nghb[0])

	event_date = ""
	if user['role'] == "host":
		djs = Dj.objects.all().reverse()
		if "event_id" in request.GET:
			event_id = request.GET['event_id']
		if "event_date" in request.GET and request.GET["event_date"] != "":
			event_date = request.GET['event_date']

			date = event_date.split("/")
			date = "%s-%s-%s 00:01" % (date[2], date[0], date[1])
			date_obj = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M")

			items = []
			for dj in djs:
				schedules = Schedule.objects.filter(dj=dj, start_date__lt=date_obj, end_date__gt=date_obj, availability=True)

				if len(schedules) > 0:
					items.append(dj)

			djs = items

		djs = djs[:settings.NUMBER_OF_ITEM_PER_PAGE]
	else:
		djs = Event.objects.filter(status=0).reverse()[:settings.MAX_ITEMS]

	page = 1
	param = "advanced=0&city=&price_range=0%3B100&booked_num=&event_type_label=&contract_num=&bydate=" + event_date

	return render_to_response('search/dashboard.html', locals(), context_instance=RequestContext(request))

@login_required()
def load_data(request):
	user = request.session['user']

	param = request.GET
	
	page = 1
	items = getItems(user['role'], param, page, int(user["id"]))

	param = urllib.urlencode(param)
	param = re.sub("&page=[\d]+", '', param)
	param = re.sub("\?page=[\d]+", '', param)

	event_id = request.GET["event_id"]

	loadmore = False

	return render_to_response('search/search_item.html', locals(), context_instance=RequestContext(request))

@login_required()
def loaddata_event(request):
	user = request.session['user']

	param = request.GET
	
	query = Q(status=0)
	# search by city
	if param["city"] != "":
		city = param["city"].split(",")
		query &= Q(address__city__icontains=city[0].strip())

	# search by price range
	price_range = param["price_range"].split(";")
	query &= Q(price__gt=int(price_range[0])) & Q(price__lt=int(price_range[1]))

	# search by city
	if param["bydate"] != "":
		date_range = param["bydate"].split("~")
		
		query &= Q(date__gt=date_range[0].strip()) & Q(date__lt=date_range[1].strip())

	items = Event.objects.filter(query).reverse()[:settings.MAX_ITEMS]	

	event_type = [item for item in param.getlist("event_type") if item != ""]
	genre = [item for item in param.getlist("genre") if item != ""]

	result = []
	
	for item in items:
		flag = 0
		if item.event_type == None or \
				(len(event_type) > 0 and not set(event_type).intersection(item.event_type.split(","))):
			flag = 1
		
		if item.genre == None or \
				(len(genre) > 0 and not set(genre).intersection(item.genre.split(","))):
			flag = 1

		if flag == 0:
			result.append(item)	

	items = result
	return render_to_response('search/search_event.html', locals(), context_instance=RequestContext(request))

@login_required()
def load_next_page(request):
	user = request.session['user']
	loadmore = True

	event_id = ""
	if "event_id" in request.GET:
		event_id = request.GET['event_id']

	page = int(request.GET['page']) + 1
	items = getItems(user['role'], request.GET, page, int(user["id"]))

	return render_to_response('search/search_item.html', locals(), context_instance=RequestContext(request))

@login_required()
def loadmore_json(request):
	user = request.session['user']
	loadmore = True

	page = int(request.GET['page']) + 1
	items = getItems(user['role'], request.GET, page, int(user["id"]))

	locations = [ {"rate": item.rate, "lat": item.person.address.lat, "lng": item.person.address.lng} \
					for item in items]
	
	return HttpResponse(json.dumps({"data": locations, "page": page}))

@login_required()
def detail(request):
	id = request.GET["id"]
	user = request.session['user']
	price = settings.PRICE

	print user["role"]
	if user["role"] == "host" and 'invite' not in request.GET:
		dj = Dj.objects.get(pk=id)
		equipments = Equipped.objects.filter(dj=dj)
		neighborhoods = Dj.objects.filter(person__address__city=dj.person.address.city)
		photos = Photo.objects.filter(dj=dj)
		event_id = request.GET["event_id"].split("?block=")[0]
		bid = []

		if event_id != "":
			event = Event.objects.get(pk=event_id)
			bid = Bid.objects.filter(event=event, dj_id=dj)

		host = Host.objects.get(person_id=user['id'])
		reviews = Review.objects.filter(host=host).order_by("-created_on")
		return render_to_response('search/dj_detail.html', locals(), context_instance=RequestContext(request))
	else:
		event = Event.objects.get(pk=id)

		rate = event.price
		time_interval = event.end_time.hour - event.start_time.hour
		total = rate * time_interval
		fee = total * 0.1
		benefit = total - fee

		if 'invite' not in request.GET:
			dj = Dj.objects.get(person_id=user['id'])
		else:
			dj = Dj.objects.get(pk=request.GET['dj_id'])

		bid = Bid.objects.filter(event=event, dj_id=dj)
		if len(bid) > 0:
			bidded = 1
			bid = bid[0]

			if bid.status == 5 or bid.status == 4:
				booking = Booking.objects.filter(bid=bid)[0]
		else:
			bidded = 0

			if request.POST or 'invite' in request.GET:
				bid = Bid()

				if 'price' in request.POST:
					bid.hourly_rate = int(request.POST['price'])
				else:
					bid.hourly_rate = event.price
					bid.status = 3 # invite a dj

				if 'description' in request.POST:
					bid.message = request.POST['description']
				else:
					bid.message = "Hi, " + dj.person.first_name + "! I'd like to invite you for my party."

				bid.price = bid.hourly_rate * time_interval
				bid.event = event
				bid.dj = dj
				bid.save()

				if 'invite' in request.GET:
					nf = Notification()
					nf.receiver = dj.person
					nf.sender = event.host.person.id
					nf.content = "%s %s would like to invite you for '%s' event." % (event.host.person.first_name, event.host.person.last_name, event.title)
					nf.url = "/search/detail?id=%d" % event.id
					nf.save()

					return redirect("/events/detail?id=%d" % event.id)

				else:
					nf = Notification()
					nf.sender = dj.person
					nf.receiver = event.host.person.id
					nf.content = "%s %s would like to apply to '%s' event." % (dj.person.first_name, dj.person.last_name, event.title)
					nf.url = "/events/detail?id=%d" % event.id
					nf.save()

				return redirect("/booking/list")

		dj = Dj.objects.get(person_id=user['id'])
		reviews = Review.objects.filter(dj=dj).order_by("-created_on")
		return render_to_response('search/event_detail.html', locals(), context_instance=RequestContext(request))


def getItems(role, param, page, id):
	query = Q()
	items = []

	# search by city
	if param["city"] != "":
		city = param['city'].split(",")
		query |= Q(person__address__city__icontains=city[0].strip())

	# search by price range
	price_range = param["price_range"].split(";")
	query &= Q(rate__gt=int(price_range[0])) & Q(rate__lt=int(price_range[1]))

	#search by contract num
	if param["advanced"] == "1" and param["booked_num"] != "" and role == "host":
		query &= Q(booked_num__gt=int(param["booked_num"]))

	#search by booked num
	if param["advanced"] == "1" and param["contract_num"] != "" and role == "host":
		try:
			query &= Q(transactions__gt=int(param["contract_num"]))
		except:
			pass

	if role == "host":
		if page == 1:
			items = Dj.objects.filter(query).reverse()[:settings.NUMBER_OF_ITEM_PER_PAGE]
		else:
			items = Dj.objects.filter(query).reverse()[:settings.MAX_ITEMS]		

	else:
		pass

	event_type = [item for item in param.getlist("event_type") if item != ""]
	genre = [item for item in param.getlist("genre") if item != ""]
	equipment = [item for item in param.getlist("equipment") if item != ""]

	result = []
	
	bydate = param["bydate"].split("?block=")[0]
	
	for item in items:
		flag = 0
		if len(event_type) > 0 and not set(event_type).intersection(item.event_type.split(",")):
			flag = 1
		
		if len(genre) > 0 and not set(genre).intersection(item.genre.split(",")):
			flag = 1

		if role == "host" and bydate.strip() != "":
			date = bydate.split("/")
			date = "%s-%s-%s 00:01" % (date[2], date[0], date[1])
			date_obj = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M")

			schedules = Schedule.objects.filter(dj=item, start_date__lt=date_obj, end_date__gt=date_obj, availability=True)

			if len(schedules) == 0:
				flag = 1

		if param["advanced"] == "1":
			equipments = Equipped.objects.filter(dj=item)
			equipment_list = [eq.equipment.name for eq in equipments]

			if len(equipment) > 0 and not set(equipment).intersection(equipment_list):
				flag = 1

		if flag == 0:
			result.append(item)

	paginator = Paginator(result, settings.NUMBER_OF_ITEM_PER_PAGE)

	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		items = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		items = []

	return items