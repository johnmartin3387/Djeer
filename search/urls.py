from django.conf.urls import url

from search import views

urlpatterns = [
    url(r'^dashboard$', views.dashboard, name="dashboard"),
    url(r'^loaddata$', views.load_data, name="loaddata"),
    url(r'^loaddata_event$', views.loaddata_event, name="loaddata_event"),
    url(r'^loadmore$', views.load_next_page, name="loadmore"),

    url(r'^loadmore_json$', views.loadmore_json, name="loadmore_json"),

    url(r'^detail$', views.detail, name="search_detail"),
]

