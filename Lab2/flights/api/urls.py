from django.conf.urls import url
import api.views as views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    
    url(r'^flights/([0-9]+)', views.flights_update,
            name='flights_update'),
    url(r'^flights', views.flights,
        name='flights'),

    url(r'^airports/([0-9]+)', views.airports_remove,
        name='airports_remove'),
    url(r'^airports/search', views.airports_search, name='airports_search'),
    url(r'^airports', views.airports, name='airports'),

    url(r'^airplanes/([0-9]+)', views.airplanes_remove,
        name='airplanes_remove'),
    url(r'^airplanes/search', views.airplanes_search, name='airplanes_search'),
    url(r'^airplanes', views.airplanes, name='airplanes'),

    url(r'^pilots/([0-9]+)', views.pilots_remove, name='pilots_remove'),
    url(r'^pilots/search', views.pilots_search, name='pilots_search'),
    url(r'^pilots', views.pilots, name='pilots')

]
