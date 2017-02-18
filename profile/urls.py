from django.conf.urls import url

from profile import views

urlpatterns = [
    url(r'^detail$', views.profile, name="profile"),

    url(r'^calendar$', views.calendar, name="calendar"),
    url(r'^update_calendar$', views.update_calendar, name="update_calendar"),
    url(r'^get_calendar_data$', views.get_calendar_data, name="get_calendar_data"),

    url(r'^save_profile$', views.save_profile, name="save_profile"),
]

