from django.shortcuts import render_to_response, redirect
from djeer_auth.models import *
from django.template import RequestContext
from django.contrib.auth.models import *

from functools import wraps

import datetime
from django.http import HttpResponse

from djeer_auth.models import *
from djeer import settings

import json
from django.views.decorators.csrf import csrf_exempt

from allauth.socialaccount.models import SocialAccount

from django.db.models import Q

# Login Required decorator
def login_required():
    def login_decorator(function):
        @wraps(function)
        def wrapped_function(request):

            # if a user is not authorized, redirect to login page
            if 'user' not in request.session or request.session['user'] is None:
                return redirect("/login")
            # otherwise, go on the request
            else:
                return function(request)

        return wrapped_function

    return login_decorator


# login view
def login(request):
    error = 'none'

    if 'email' in request.POST:

        # get username and password from request.
        email = request.POST['email']
        password = request.POST['password']

        # get a user from database based on username and password
        user = Person.objects.filter(email=email, password=password)

        # check whether the user is in database or not
        if len(user) < 1:
            error = 'block'
        else:
            request.session['user'] = {
                "id": user[0].id,
                "email": user[0].email,
                "role": user[0].role,
                "image": user[0].image,
                "name": user[0].first_name,
                "password": user[0].password,
                "chat": user[0].chat
            }

            if user[0].role == 'dj':
                return redirect("/search/dashboard")

            return redirect("/")

    return render_to_response('auth/login.html', {'error':error}, context_instance=RequestContext(request))


# logout view
#   initialize session variable
def logout(request):
    request.session['user'] = None
    return redirect("/login")


def main_page(request):

    if 'user' in request.session and request.session['user'] is not None and request.session['user']['role'] == 'dj':
        return redirect("/search/dashboard")
    
    genre = settings.GENRE
    items = Dj.objects.all().order_by("transactions")[:12]
    param = {"place": "", "genre": "", "date": ""}
    if request.POST:
        param = request.POST

        items = []
        query = Q()
        # search by city
        if param["place"] != "":
            query |= Q(person__address__city__icontains=param["place"])

        # search by city
        if param["genre"] != "":
            query &= Q(genre__icontains=param["genre"])

        djs = Dj.objects.filter(query).order_by("transactions")

        if param["date"] != "":
            date = param["date"].split("/")
            date = "%s-%s-%s 00:01" % (date[2], date[0], date[1])
            date_obj = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M")

            for dj in djs:
                schedules = Schedule.objects.filter(dj=dj, start_date__lt=date_obj, end_date__gt=date_obj, availability=True)
                
                if len(schedules) > 0:
                    items.append(dj)
            items = items[:12]
        else:
            items = djs

    return render_to_response('main.html', locals(), context_instance=RequestContext(request))

@login_required()
def index_page(request):
    user = request.session['user']

    email = user["email"]
    role = user["role"]

    person = Person.objects.get(pk=user["id"])
    if role == "dj":
        user = Dj.objects.filter(person_id=user["id"])[0]
    else:
        user = Host.objects.filter(person_id=user["id"])[0]

    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def signup(request, person):
    person = person
    return render_to_response('auth/signup.html', locals(), context_instance=RequestContext(request))

# sign up a user
def signup_djeer(request, person):

    try:
        tp_user = User.objects.filter(username=request.user)
        fb_account = SocialAccount.objects.filter(user=tp_user[0])[0]
        user = fb_account.extra_data

    except:
        user = dict()

    person = person

    country_name = settings.COUNTRY
    genre = settings.GENRE
    event_type = settings.EVENT_TYPE
    rate = settings.PRICE

    if request.POST:

        # create an address
        address = Address()
        address.street = request.POST["address"]
        address.city = request.POST["city"]
        address.state = request.POST["state"]
        address.country = request.POST["country"]
        address.zip_code = request.POST["zipcode"]
        address.lat = request.POST["lat"]
        address.lng = request.POST["lng"]
        address.save()

        dup_person = Person.objects.filter(email=request.POST["email"])
        if len(dup_person) > 0:
            return render_to_response('auth/signup_djeer.html', locals(), context_instance=RequestContext(request))

        # create person
        person = Person()

        person.email = request.POST["email"]
        person.password = request.POST["password"]
        person.first_name = request.POST["firstname"]
        person.last_name = request.POST["lastname"]
        person.gender = int(request.POST["gender"])

        birthday = request.POST["birthday"].split("/")
        birthday = "%s-%s-%s 00:00" % (birthday[2], birthday[0], birthday[1])
        person.birthday = birthday
        person.chat = request.POST['chat_id']

        person.phone = request.POST["phone"]
        person.image = request.POST['chat_id']
        if "profile_image" in request.FILES:
            person.image = save_file(request.FILES["profile_image"], image_id=address.id, filename=request.POST['chat_id'])

        person.role = request.POST["role"]
        person.active = True

        person.description = request.POST["description"]

        person.address = address
        person.save()

        request.session['user'] = {
            "id": person.id,
            "email": person.email,
            "role": person.role,
            "image": person.image,
            "name": person.first_name,
            "password": person.password,
            "chat": person.chat
        }

        # create djeer user
        if person.role == "dj":
            dj = Dj()
            dj.person = person
            dj.title = request.POST["profile_title"]
            dj.rate = request.POST["profile_rate"]
            dj.discount_rate = 0 #request.POST["discount_rate"]
            dj.discount_hour = 0 #request.POST["discount_hour"]
            dj.genre = ','.join(request.POST.getlist('genre'))
            dj.event_type = ','.join(request.POST.getlist('event_type'))
            dj.save()

            if 'images[]' in request.FILES:
                for image in request.FILES.getlist('images[]'):
                    photo = Photo()
                    photo.photo_url = save_file(image, image_id=dj.id)
                    photo.dj = dj
                    photo.save()

            equipment = request.POST["equipment"].split(",")
            for eq in equipment:
                eq_obj = Equipment.objects.filter(name=eq)
                if len(eq_obj) == 0:
                    eq_obj = Equipment()
                    eq_obj.name = eq
                    eq_obj.save()
                else:
                    eq_obj = eq_obj[0]

                equipped = Equipped()
                equipped.equipment = eq_obj
                equipped.dj = dj
                equipped.save()

            return redirect("/search/dashboard")
        else:
            host = Host()
            host.event_type = "" #request.POST["event_type"]
            host.genre = "" #request.POST["genre"]
            host.person = person
            host.save()

            return redirect("/")
        
    return render_to_response('auth/signup_djeer.html', locals(), context_instance=RequestContext(request))


def save_file(file, path='images', image_id=0, filename=""):
    temp = settings.BASE_DIR + settings.STATIC_URL + str(path)

    if not os.path.exists(temp):
        os.makedirs(temp)

    if filename == "":
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

# check email duplication
@csrf_exempt
def check_duplication(request):
    res = {"result": "false"}

    email = request.POST["email"]
    if len(Person.objects.filter(email=email)) > 0:
        res["result"] = "true"

    return HttpResponse(json.dumps(res)) 
