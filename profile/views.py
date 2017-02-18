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

@login_required()
def profile(request):
    user = request.session['user']
    menu = "profile"

    email = user["email"]
    role = user["role"]
    person = Person.objects.get(pk=user["id"])

    birthday = person.birthday.strftime("%m/%d/%Y")

    country_name = settings.COUNTRY
    genre = settings.GENRE
    event_type = settings.EVENT_TYPE
    rate = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]

    if role == "dj":
        user = Dj.objects.filter(person_id=user["id"])[0]
        equipments = Equipped.objects.filter(dj=user)
        equipments = [eq.equipment.name for eq in equipments]
        equipments = ",".join(equipments)

        photos = Photo.objects.filter(dj=user)
        reviews = Review.objects.filter(dj=user).order_by("-created_on")

    else:
        user = Host.objects.filter(person_id=user["id"])[0]
        reviews = Review.objects.filter(host=user).order_by("-created_on")

    selected_genre = user.genre.split(",")
    selected_event_type = user.event_type.split(",")

    tab = "1"
    if "tab" in request.GET:
        tab = request.GET['tab']

    return render_to_response('profile/profile.html', locals(), context_instance=RequestContext(request))

@login_required()
def calendar(request):
    menu = "calendar"
    return render_to_response('profile/calendar.html', locals(), context_instance=RequestContext(request))

@login_required()
def save_profile(request):
    user = request.session['user']

    email = user["email"]
    role = user["role"]
    person = Person.objects.get(pk=user["id"])

    if role == "dj":
        user = Dj.objects.filter(person_id=user["id"])[0]
    else:
        user = Host.objects.filter(person_id=user["id"])[0]

    tab = int(request.POST['profile_tab'])

    if tab == 1:
        # person.email = request.POST["email"]
        person.first_name = request.POST["firstname"]
        person.last_name = request.POST["lastname"]
        person.gender = int(request.POST["gender"])
        person.chat = int(request.POST["chat_id"])

        birthday = request.POST["birthday"].split("/")
        birthday = "%s-%s-%s 00:00" % (birthday[2], birthday[0], birthday[1])
        person.birthday = birthday

        person.phone = request.POST["phone"]
        if "profile_image" in request.FILES:
            person.image = save_file(request.FILES["profile_image"], image_id=person.address.id)
            request.session["user"]["image"] = person.image
            print request.session["user"]

        person.address.street = request.POST["address"]
        person.address.city = request.POST["city"]
        person.address.state = request.POST["state"]
        person.address.country = request.POST["country"]
        person.address.zip_code = request.POST["zipcode"]
        person.address.lat = request.POST["lat"]
        person.address.lng = request.POST["lng"]
        person.address.save()

        request.session["user"]["name"] = request.POST["firstname"]
        request.session.modified = True

        person.save()

    elif tab == 2:
        if role == "dj":
            print request.POST["profile_rate"]
            
            user.title = request.POST["profile_title"]
            user.rate = request.POST["profile_rate"]
            user.discount_rate = 0 #request.POST["discount_rate"]
            user.discount_hour = 0 #request.POST["discount_hour"]
            user.genre = ','.join(request.POST.getlist('genre'))
            user.event_type = ','.join(request.POST.getlist('event_type'))
            user.save()

            person.description = request.POST["description"]
            person.save()

            Equipped.objects.filter(dj=user).delete()
            equipment = request.POST["equipment"].split(",")
            for eq in equipment:
                eq_obj = Equipment.objects.filter(name=eq)
                if len(eq_obj) == 0:
                    eq_obj = Equipment()
                    eq_obj = eq
                    eq_obj.save()
                else:
                    eq_obj = eq_obj[0]

                equipped = Equipped()
                equipped.equipment = eq_obj
                equipped.dj = user
                equipped.save()

        else:
            person.description = request.POST["description"]
            person.save()

            user.genre = "" #request.POST['genre']
            user.event_type = "" #request.POST['event_type']
            user.save()

    elif tab == 3:

        Photo.objects.filter(dj=user).delete()

        index = 0
        while True:
            photo = Photo()

            tag = 'image[%d]' % index
            if tag in request.FILES:
                photo.photo_url = save_file(request.FILES[tag], image_id=user.id)
            else:
                photo.photo_url = request.POST['profile_image_existed[%d]' % index]

            photo.dj = user
            photo.save()

            index += 1
            if 'profile_image_existed[%d]' % index not in request.POST:
                break                

        if 'images[]' in request.FILES:
            for image in request.FILES.getlist('images[]'):
                photo = Photo()
                photo.photo_url = save_file(image, image_id=user.id)
                photo.dj = user
                photo.save()

    return redirect("/profile/detail?tab=%d" % tab)


def save_file(file, path='images', image_id=0):
    temp = settings.BASE_DIR + settings.STATIC_URL + str(path)

    if not os.path.exists(temp):
        os.makedirs(temp)

    filename_tp = file._get_name().split(".")
    filename = ""
    filename = filename_tp[0] + "_" + str(image_id)
    if len(filename_tp) > 1:
        filename += "." + filename_tp[1]
    
    fd = open('%s/%s' % (temp, str(filename)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()

    return filename

@login_required()
@csrf_exempt
def update_calendar(request):
	user = request.session['user']
	if user['role'] != "dj":
		return HttpResponse('{"res": "failed"}') 

	res = {"res": "success"}

	try:
		data = json.loads(request.POST['data'])
	except:
		data = []
	
	person = Person.objects.get(pk=user["id"])
	user = Dj.objects.filter(person_id=user["id"])[0]

	# delete all schedules that are related to this user.
	Schedule.objects.filter(dj=user).delete()
	for item in data:
		schedule = Schedule()
		tokens = item['title'].split(" ")
		if tokens[0] == "Available":
			schedule.availability = True
			try:
				schedule.rate = int(tokens[1][1:])
			except:
				schedule.rate = 0
		else:
			schedule.availability = False
			schedule.rate = 0

		schedule.start_date = item["start_date"]
		schedule.end_date = item["end_date"]
		schedule.dj = user

		schedule.save()

	return HttpResponse(json.dumps(res)) 
	
@login_required()
def get_calendar_data(request):
	user = request.session['user']
	person = Person.objects.get(pk=user["id"])
	user = Dj.objects.filter(person_id=user["id"])[0]

	res = []

	current_date = datetime.datetime.now()
	schedules = Schedule.objects.filter(dj=user, end_date__gt=current_date)

	for item in schedules:
		token = dict()

		if item.availability:
			token["title"] = "Available $%d" % item.rate
			token["backgroundColor"] = "#1bbc9b"
		else:
			token["title"] = "Unavailable"
			token["backgroundColor"] = "#F3565D"

		start_date = item.start_date.strftime("%Y-%m-%d")
		end_date = item.end_date.strftime("%Y-%m-%d")

		token["start"] = start_date
		if start_date != end_date:
			token["end"] = end_date

		res.append(token)

	return HttpResponse(json.dumps(res)) 