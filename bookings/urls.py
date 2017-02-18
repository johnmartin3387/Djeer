from django.conf.urls import url

from bookings import views

urlpatterns = [
    url(r'^list$', views.booking_list, name="booking_list"),
    url(r'^create$', views.booking_create, name="booking_create"),
    url(r'^handle_offer$', views.handle_offer, name="handle_offer"),

    url(r'^end_contract$', views.end_contract, name="end_contract"),

    url(r'^setup_payment$', views.setup_payment, name="setup_payment")
]

