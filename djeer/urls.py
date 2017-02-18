from django.conf.urls import url, include

from djeer_auth import views
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.main_page, name="main"),

    url(r'^lostpet_admin_login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^signup/(?P<person>[0-9a-z]+)$', views.signup, name="signup"),
    url(r'^signup_djeer/(?P<person>[0-9a-z]+)$', views.signup_djeer, name="signup_djeer"),

    url(r'^auth/', include('djeer_auth.urls')),
    url(r'^profile/', include('profile.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^search/', include('search.urls')),
    url(r'^chat/', include('message.urls')),
    url(r'^booking/', include('bookings.urls')),
    url(r'^help/', include('help.urls')),

    url(r'^djeer/index/$', views.index_page, name="index"),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^tinymce/$', include('tinymce.urls')),
]

