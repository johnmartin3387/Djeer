from django.conf.urls import url

from djeer_auth import views

urlpatterns = [
    url(r'^duplication/$', views.check_duplication, name="duplication"),
]

