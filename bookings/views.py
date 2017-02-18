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
from django.contrib.auth import logout

from djeer_auth.views import login_required
from allauth.socialaccount.models import SocialAccount

import stripe

@login_required()
def booking_list(request):
    user = request.session['user']

    if user['role'] == "host":
        return redirect("/login")

    dj = Dj.objects.get(person__id=user['id'])
    normal = Bid.objects.filter(dj=dj, status__lt=4).exclude(status=1)
    bookings = Bid.objects.filter(dj=dj, status=4)
    offers = Bid.objects.filter(dj=dj, status=5)
    feedbacks = Booking.objects.filter(bid__dj=dj, status=4)

    return render_to_response('bookings/list.html', locals(), context_instance=RequestContext(request))

@login_required()
def booking_create(request):
    user = request.session['user']
    if user['role'] != "dj":
        redirect("/login")

    bid_id = request.GET["bid_id"]
    bid = Bid.objects.get(pk = bid_id)

    bk = Booking.objects.filter(bid=bid)
    price = settings.PRICE

    if len(bk) > 0:
        error = True
        return render_to_response('bookings/create.html', locals(), context_instance=RequestContext(request))

    error = False
    rate = bid.hourly_rate
    time_interval = bid.event.end_time.hour - bid.event.start_time.hour
    total = rate * time_interval
    fee = total * 0.1
    benefit = total - fee

    
    if request.POST:

        booking = Booking()
        booking.bid = bid
        booking.event = bid.event
        booking.price = request.POST['price']
        booking.message = request.POST['description']
        booking.hours = request.POST['hours']
        booking.status = 0 

        bid.event.status = 0
        bid.event.save()

        bid.status = 5
        bid.save()

        booking.save()

        nf = Notification()
        nf.receiver = booking.bid.dj.person
        nf.sender = booking.bid.event.host.person.id
        nf.content = "%s %s sent you an offer for '%s' event." % (booking.bid.event.host.person.first_name, booking.bid.event.host.person.last_name, booking.bid.event.title)
        nf.url = "/search/detail?id=%d" % booking.bid.event.id
        nf.save()

        return redirect("/events/list")

    return render_to_response('bookings/create.html', locals(), context_instance=RequestContext(request))

@login_required()
def handle_offer(request):
    user = request.session['user']

    if user['role'] == "host":
        return redirect("/login")

    if 'options' in request.GET:
        booking = Booking.objects.get(pk=request.GET['booking_id'])
        if request.GET['options'] == 'accept':
            dj = Dj.objects.get(person__id=user['id'])

            if dj.stripe_uid in [None, ""]:
            	logout(request)
                return redirect("/accounts/stripe/login/?process=login&next=/booking/setup_payment?booking_id=" + str(request.GET['booking_id']))

            booking.status = 1
            booking.save()

            booking.bid.status = 4
            booking.bid.save()

            booking.bid.event.status = 1
            booking.bid.event.save()

            if booking.bid.dj.booked_num == None:
                booking.bid.dj.booked_num = 1
            else:
                booking.bid.dj.booked_num += 1

            booking.bid.dj.save()

            nf = Notification()
            nf.receiver = booking.bid.event.host.person
            nf.sender = booking.bid.dj.person.id
            nf.content = "%s %s accepted your offer for '%s' event. Contract is started." % (booking.bid.dj.person.first_name, booking.bid.dj.person.last_name, booking.bid.event.title)
            nf.url = "/events/detail?id=%d" % booking.bid.event.id
            nf.save()

            bids = Bid.objects.filter(event=booking.event, status__in=[0, 3])
            for bid in bids:
                bid.status = 1
                bid.message = "Choose another dj."
                bid.save()

                nf = Notification()
                nf.sender = bid.event.host.id
                nf.receiver = bid.dj.person
                nf.content = "Proposal Ended: %s. Reason: Hire another freelancer." % (bid.event.title)
                nf.url = ""
                nf.save()
        else:
            booking.status = 3
            booking.save()

            booking.bid.status = 1
            booking.bid.message = "Sorry!"
            booking.bid.save()

            booking.bid.event.status = 0
            booking.bid.event.save()

    return redirect("/booking/list")


def setup_payment(request):

    tp_user = User.objects.filter(username=request.user)
    stripe_uid = SocialAccount.objects.filter(user=tp_user[0], provider="stripe")[0]	
    data = stripe_uid.extra_data

    dj = Dj.objects.get(person__email=data['email'])
    dj.stripe_uid = stripe_uid.uid
    dj.save()

    request.session['user'] = {
        "id": dj.person.id,
        "email": dj.person.email,
        "role": dj.person.role,
        "image": dj.person.image,
        "name": dj.person.first_name
    }

    return redirect("/booking/handle_offer?options=accept&booking_id=" + request.GET['booking_id'])

@login_required()
def end_contract(request):
	user = request.session['user']

	if user['role'] == "dj":
		role = "host"
	else:
		role = "dj"

	if request.GET:
		booking_id = request.GET['booking_id']

		booking = Booking.objects.get(pk=booking_id)

		if len(Review.objects.filter(booking=booking, role=role, success="success")):
			if user['role'] == "host":
				return redirect("/events/list")
			else:
				return redirect("/booking/list")

		if len(Review.objects.filter(booking=booking, role=role)) == 0:

			if 'token' in request.GET:
				amount = int(float(booking.price * booking.hours) * 100)
				stripe.api_key = settings.STRIPE_SECRET_KEY

				print booking.bid.dj.stripe_uid
				charge = stripe.Charge.create(
					amount=amount,
					currency="usd",
					source=request.GET['token'],
					destination=booking.bid.dj.stripe_uid,
					application_fee = int(amount * 0.1),
					description='Sent the money!'
				)

				nf = Notification()
				nf.sender = booking.bid.event.host.person.id
				nf.receiver = booking.bid.dj.person
				nf.content = "%s %s paid $%d for '%s' event. Contract is ended." % (booking.bid.event.host.person.first_name, booking.bid.event.host.person.last_name, amount, booking.bid.event.title)
				nf.url = ""
				nf.save()

			booking.status = 4
			booking.save()

			booking.bid.status = 6
			booking.bid.save()

			booking.event.status = 2
			booking.event.save()
			

			review = Review()
			review.success = "no feedback"
			review.booking = booking

			if user['role'] == "dj":
				review.role = "host"
			else:
				review.role = "dj"

				if booking.bid.dj.transactions == None:
					booking.bid.dj.transactions = 1
				else:
					booking.bid.dj.transactions += 1

				booking.bid.dj.save()

			# review.transaction_id = ""
			# review.paid_out = ""
			review.save()
		else:
			review = Review.objects.filter(booking=booking, role=role)

	elif request.POST:

		review = Review.objects.filter(booking_id=int(request.POST['booking_id']), role=role)[0]

		booking = Booking.objects.get(pk=int(request.POST['booking_id']))
		review.feedback = request.POST['description']

		if user['role'] == "host":
			review.dj = booking.bid.dj
			scores = [float(request.POST['communication']) / 2.0, float(request.POST['professionalism']) / 2, \
				float(request.POST['accuracy']) / 2.0, float(request.POST['track']) / 2.0, \
				float(request.POST['communication']) / 2.0, float(request.POST['value']) / 2.0]

			review.track = scores[3]
			review.mixing = scores[4]
			review.value = scores[5]
		else:
			review.host = booking.bid.event.host
			scores = [float(request.POST['communication']) / 2.0, float(request.POST['professionalism']) / 2, \
				float(request.POST['accuracy']) / 2.0]

		review.communication = scores[0]
		review.professionalism = scores[1]
		review.accuracy = scores[2]
		
		review.score = sum(scores) * 1.0 / len(scores)
		review.success = "success"

		# review.booking.bid.dj
		# review.amount = review.booking.
		

		review.save()

		if user["role"] == "dj":
			booking.status = 2
			booking.save()

			booking.bid.status = 7
			booking.bid.save()

		booking.bid.dj.score = booking.bid.dj.score * (booking.bid.dj.transactions - 1) + \
									review.score/ booking.bid.dj.transactions
		booking.bid.dj.save()

		if user['role'] == "host":
			return redirect("/events/list")
		else:
			return redirect("/booking/list")

	return render_to_response('bookings/feedback.html', locals(), context_instance=RequestContext(request))

