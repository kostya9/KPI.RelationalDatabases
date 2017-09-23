from django.conf.urls import url
import api.views as views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^airports/', views.airports, name='airports'),
    url(r'^airplanes/', views.airplanes, name='airplanes'),
    url(r'^pilots/', views.pilots, name='pilots')

]