from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from api.repositories.pilots import Pilots
from api.repositories.airplanes import Airplanes 
from api.repositories.airports import Airports 
from api.repositories.flights import Flights 

from wsgiref.util import FileWrapper
from io import StringIO

import MySQLdb
from api.models import Encoder, Pilot, Flight, Airplane, Airport
import json

import simplexml

import datetime

def connect():
    db = MySQLdb.connect(host="localhost",
                     user="root",
                     db="flights")
    db.set_character_set('utf8')
    return db

# Create your views here.
def index(request: HttpRequest):
    if request.method == 'GET':
        return JsonResponse({'text': '123'})

@method_decorator(csrf_exempt, name='dispatch')
def pilots(request: HttpRequest):
    if request.method == 'GET':
        with connect() as connection:
            repository = Pilots(connection)
            pilots = repository.all()
        return JsonResponse(pilots, safe=False, encoder=Encoder)
    elif request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        pilot = json.loads(body_unicode)
        try:
            firstname = pilot["firstname"].encode('utf-8')
            lastname = pilot["lastname"].encode('utf-8')
            start_date = pilot["startdate"]
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            pilot = Pilot(0, firstname, lastname, start_date)
        except TypeError as e:
            print(e)
            return HttpResponse(status=400)
        with connect() as connection:
            repository = Pilots(connection)
            repository.add(pilot)
        return HttpResponse(status=200)

def pilots_search(request: HttpRequest):
    if request.method == 'GET':
        with connect() as connection:
            repository = Pilots(connection)
            firstname = request.GET.get('firstname')
            lastname = request.GET.get('lastname')
            pilots = repository.search(firstname, lastname)
        return JsonResponse(pilots, safe=False, encoder=Encoder)

def pilots_export(request: HttpRequest):
    with connect() as connection:
        repository = Pilots(connection)
        pilots = repository.all()
    return export(request, pilots, 'pilots')

@method_decorator(csrf_exempt, name='dispatch')
def pilots_import(request: HttpRequest):
    if request.method == 'POST':
        body = request.FILES["file"].read()
        print(body)
        pilots_dict = simplexml.loads(body)['pilots']
        print(pilots_dict)
        pilots = [Pilot(0, p['firstname'], p['lastname'], p['starting_date']) for p in pilots_dict]
        with connect() as connection:
            repository = Pilots(connection)
            repository.import_all(pilots)
        return HttpResponse(status=200)


@method_decorator(csrf_exempt, name='dispatch')
def pilots_remove(request: HttpRequest, id):
    if request.method == 'DELETE':
        with connect() as connection:
            repository = Pilots(connection)
            repository.remove(id)
        return HttpResponse(status=200)

@method_decorator(csrf_exempt, name='dispatch')
def airports(request: HttpRequest):
    if request.method == 'GET':
        with connect() as connection:
            repository = Airports(connection)
            airports = repository.all()
        return JsonResponse(airports, safe=False, encoder=Encoder)

def airports_search(request: HttpRequest):
    if request.method == 'GET':
        with connect() as connection:
            repository = Airports(connection)
            name = request.GET.get('name')
            code = request.GET.get('code')
            city = request.GET.get('city')
            airports = repository.search(name, code, city)
        return JsonResponse(airports, safe=False, encoder=Encoder)

@method_decorator(csrf_exempt, name='dispatch')
def airports_remove(request: HttpRequest, id):
    if request.method == 'DELETE':
        with connect() as connection:
            repository = Airports(connection)
            repository.remove(id)
        return HttpResponse(status=200)

def airports_export(request: HttpRequest):
    with connect() as connection:
        repository = Airports(connection)
        airports = repository.all()
    return export(request, airports, 'airports')

@method_decorator(csrf_exempt, name='dispatch')
def airports_import(request: HttpRequest):
    if request.method == 'POST':
        body = request.FILES["file"].read()
        airports_dict = simplexml.loads(body)['airports']
        airports = [Airport(0, a['name'], a['code'], a['city']) for a in airports_dict]
        with connect() as connection:
            repository = Airports(connection)
            repository.import_all(airports)
        return HttpResponse(status=200)

@method_decorator(csrf_exempt, name='dispatch')
def airplanes(request: HttpRequest):
    if request.method == 'GET':
        with connect() as connection:
            repository = Airplanes(connection)
            airplanes = repository.all()
        return JsonResponse(airplanes, safe=False, encoder=Encoder)

@method_decorator(csrf_exempt, name='dispatch')
def airplanes_remove(request: HttpRequest, id):
    if request.method == 'DELETE':
        with connect() as connection:
            repository = Airplanes(connection)
            repository.remove(id)
        return HttpResponse(status=200)


def airplanes_search(request: HttpRequest):
    if request.method == 'GET':
        with connect() as connection:
            repository = Airplanes(connection)
            build_start = request.GET.get('buildrangeStart')
            build_end = request.GET.get('buildrangeEnd')
            model_name = request.GET.get('modelname')
            airplanes = repository.search(model_name, build_start, build_end)
        return JsonResponse(airplanes, safe=False, encoder=Encoder)


def airplanes_export(request: HttpRequest):
    with connect() as connection:
        repository = Airplanes(connection)
        airplanes = repository.all()
    return export(request, airplanes, 'airplanes')

@method_decorator(csrf_exempt, name='dispatch')
def airplanes_import(request: HttpRequest):
    if request.method == 'POST':
        body = request.FILES["file"].read()
        airplanes_dict = simplexml.loads(body)['airplanes']
        airplanes = [Airplane(0, a['modelname'], a['builddate']) for a in airplanes_dict]
        with connect() as connection:
            repository = Airplanes(connection)
            repository.import_all(airplanes)
        return HttpResponse(status=200)

def dict_from_class(cls):
     return dict(
         (key, value)
         for (key, value) in cls.__dict__.items()
         )

def export(request: HttpRequest, data, name):
    if request.method == 'GET':
        data = {name: [{name[0:name.__len__() - 1]: dict_from_class(el)} for el in data]}
        export = simplexml.dumps(data)
        response = HttpResponse(export, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="%s.xml"' % (name)
        return response

def __map_body_to_flight(request: HttpRequest):
    body_unicode = request.body.decode('utf-8')
    flight = json.loads(body_unicode)

    pilot_id = flight["pilot_id"]
    air_id = flight["airplane_id"]
    dep_airp_id = flight["departure_airport_id"]
    arr_airp_id = flight["arrival_airport_id"]
    dep_time = flight["departure_time"]
    arr_time = flight["arrival_time"]

    mapped_flight = Flight(0, pilot_id, air_id, dep_airp_id, arr_airp_id, dep_time, arr_time)
    return mapped_flight

@method_decorator(csrf_exempt, name='dispatch')
def flights(request: HttpRequest):
    if request.method == 'GET':
        with connect() as connection:
            repository = Flights(connection)
            flights = repository.all()
        return JsonResponse(flights, safe=False, encoder=Encoder)
    elif request.method == 'POST':
        try:
            flight = __map_body_to_flight(request)
        except TypeError as e:
            print(e)
            return HttpResponse(status=400)
        with connect() as connection:
            repository = Flights(connection)
            repository.add(flight)
        return HttpResponse(status=200)

@method_decorator(csrf_exempt, name='dispatch')
def flights_update(request: HttpRequest, id):
    if request.method == 'PUT':
        try:
            flight = __map_body_to_flight(request)
        except TypeError as e:
            print(e)
            return HttpResponse(status=400)
        with connect() as connection:
            repository = Flights(connection)
            repository.update(id, flight)
        return HttpResponse(status=200)
    if request.method == 'DELETE':
        with connect() as connection:
            repository = Flights(connection)
            repository.remove(id)
        return HttpResponse(status=200)