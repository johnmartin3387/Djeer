from django.conf.urls import url

from message import views

urlpatterns = [
    url(r'^messages$', views.message_request, name="message"),
    url(r'^notification$', views.notification, name="notification"),
    url(r'^reset-notification$', views.reset_notification, name="reset-notification"),

    # url(r'^save-notification$', views.save_notification, name="save-notification"),
]

