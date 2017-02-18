from django.conf.urls import url

from help import views

urlpatterns = [
    url(r'^edit$', views.help_edit, name="help_edit"),
    url(r'^$', views.help_live, name="help_live"),
]