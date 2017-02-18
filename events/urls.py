from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^list$', views.event_list, name="event_list"),
    url(r'^create$', views.event_create, name="event_create"),
    url(r'^detail$', views.event_detail, name="event_detail"),
    
    url(r'^remove$', views.remove_event, name="remove_event"),
]

