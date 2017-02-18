from __future__ import unicode_literals

from django.db import models
import os

from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE

class Address(models.Model):
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    lat = models.FloatField(null=True, blank=True, default=None)
    lng = models.FloatField(null=True, blank=True, default=None)

    class Meta:
        db_table = 'Address'


class Billing(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=255)

    class Meta:
        db_table = 'Billing'


class Setting(models.Model):
    email_notification = models.CharField(max_length=255, blank=True, null=True)
    mobile_notification = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    search_engine = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Setting'


class Person(models.Model):
    bill = models.ForeignKey('Billing', blank=True, null=True)
    setting = models.ForeignKey('Setting', blank=True, null=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.IntegerField(null=True, blank=True)
    birthday = models.DateTimeField()
    phone = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)
    profile_url = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=10, blank=True, null=True)
    active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey('Address', blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    chat = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        db_table = 'Person'


class Dj(models.Model):
    person = models.ForeignKey('Person', blank=True, null=True)
    title = models.CharField(max_length=255)
    rate = models.FloatField(null=True, blank=True)
    discount_rate = models.FloatField(null=True, blank=True)
    discount_hour = models.IntegerField(null=True, blank=True)
    booked_num = models.IntegerField(null=True, blank=True)
    transactions = models.IntegerField(null=True, blank=True)
    responses = models.IntegerField(null=True, blank=True)
    avg_response_time = models.IntegerField(null=True, blank=True)

    event_type = models.TextField(null=True, blank=True)
    genre = models.TextField(null=True, blank=True)

    score = models.FloatField(null=True, blank=True, default=0)
    stripe_uid = models.CharField(max_length=255, null=True, blank=True, default=None)

    class Meta:
        db_table = 'DJ'


class Event(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(null=True, blank=True)
    date = models.DateField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100)                   # 0: no action, 1: booked, 2: finished 3: cancel
    address = models.ForeignKey('Address', blank=True, null=True)
    host = models.ForeignKey('Host', blank=True, null=True)

    event_type = models.TextField(null=True, blank=True)
    genre = models.TextField(null=True, blank=True)

    score = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        db_table = 'Event'


class Bid(models.Model):
    hourly_rate = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    message = models.TextField()
    event = models.ForeignKey('Event', blank=True, null=True)
    dj = models.ForeignKey('DJ', blank=True, null=True)
    status = models.IntegerField(null=True, blank=True, default=0) # 0: no action, 1: declined, 3: invite dj 4: booked 5: send an offer, 6: wait for feedback 7: end
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Bid'
        unique_together = (('id', 'event'),)


class Equipment(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Equipment'


class Equipped(models.Model):
    equipment = models.ForeignKey('Equipment', blank=True, null=True)
    dj = models.ForeignKey('DJ', blank=True, null=True)

    class Meta:
        db_table = 'Equipped'
        unique_together = (('equipment', 'dj'),)


class Host(models.Model):
    person = models.ForeignKey('Person', blank=True, null=True)
    event_type = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)

    class Meta:
        db_table = 'Host'


class Payment(models.Model):
    type = models.CharField(max_length=10)
    card_number = models.CharField(max_length=100)
    expires_on = models.DateTimeField(blank=True, null=True)
    security_code = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    person = models.ForeignKey('Person', blank=True, null=True)

    class Meta:
        db_table = 'Payment'


class Photo(models.Model):
    photo_url = models.CharField(max_length=255)
    dj = models.ForeignKey('DJ', blank=True, null=True)

    class Meta:
        db_table = 'Photo'


class Review(models.Model):
    feedback = models.TextField(blank=True, null=True)
    score = models.FloatField(null=True, blank=True)
    communication = models.FloatField(null=True, blank=True)            # venue
    professionalism = models.FloatField(null=True, blank=True)          # atmosphere
    accuracy = models.FloatField(null=True, blank=True)                 # venue
    track = models.FloatField(null=True, blank=True)                    
    mixing = models.FloatField(null=True, blank=True)                   
    value = models.FloatField(null=True, blank=True)                    
    success = models.CharField(max_length=50, blank=True, null=True)
    amount = models.FloatField(null=True, blank=True)
    paid_out = models.FloatField(null=True, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    booking = models.ForeignKey('Booking', blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)

    dj = models.ForeignKey('Dj', blank=True, null=True)
    host = models.ForeignKey('Host', blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Review'


class Schedule(models.Model):
    start_date = models.DateTimeField(blank=False, null=False, default=None)
    end_date = models.DateTimeField(blank=False, null=False)
    availability = models.BooleanField(default=False)
    rate = models.FloatField(null=True, blank=True)
    dj = models.ForeignKey('DJ', blank=True, null=True)

    class Meta:
        db_table = 'Schedule'

class Booking(models.Model):
    bid = models.ForeignKey('Bid', blank=True, null=True)
    event = models.ForeignKey('Event', blank=True, null=True)
    price = models.FloatField(null=True, blank=True, default=0)
    hours = models.IntegerField(null=True, blank=True, default=0)
    message = models.TextField(null=True, blank=True, default="")
    # 0: send an offer, 1: accept an offer and start contract, 2: end contract, 
    # 3: cancel, 4: wait for feedback
    status = models.CharField(max_length=10, blank=True, null=True) 

    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'booking'
        unique_together = (('bid', 'event'),)


class Notification(models.Model):
    sender = models.IntegerField(null=True, blank=True, default=None)
    receiver = models.ForeignKey('Person', blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(blank=True, null=True, default=0) 

    url = models.CharField(max_length=100, blank=True, null=True, default="")

    class Meta:
        db_table = 'Notification'


class Help(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = HTMLField(blank=True, null=True, default="")
    parent = models.ForeignKey('self', blank=True, null=True)
    sort = models.IntegerField(null=True, blank=True, default=100)

    class Meta:
        db_table = 'Help'

    def __unicode__(self):
        return u'%s' % (self.title)