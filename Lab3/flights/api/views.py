from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse

from wsgiref.util import FileWrapper
from io import StringIO

from api.models import Encoder, Pilot, Flight, Airplane, Airport
import json

import simplexml

import datetime

# Create your views here.
def index(request: HttpRequest):
    if request.method == 'GET':
        return JsonResponse({'text': '123'})

@method_decorator(csrf_exempt, name='dispatch')
def pilots(request: HttpRequest):
    if request.method == 'GET':
        pilots = list(Pilot.objects.all().values())
        return JsonResponse(pilots, safe=False, encoder=Encoder)
    elif request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        pilot = json.loads(body_unicode)
        try:
            firstname = pilot["firstname"].encode('utf-8')
            lastname = pilot["lastname"].encode('utf-8')
            start_date = pilot["startdate"]
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        except TypeError as e:
            print(e)
            return HttpResponse(status=400)
        pilot = Pilot(firstname = firstname, lastname = lastname, start_date = start_date)
        pilot.save()
        return HttpResponse(status=200)

def pilots_search(request: HttpRequest):
    if request.method == 'GET':
        firstname = request.GET.get('firstname')
        lastname = request.GET.get('lastname')
        pilots = list(Pilots.objects.filter(firstname__icontains=firstname, lastname__icontains=lastname).values())
        return JsonResponse(pilots, safe=False, encoder=Encoder)

def pilots_export(request: HttpRequest):
    pilots = list(Pilot.objects.all().values())
    return export(request, pilots, 'pilots')

@method_decorator(csrf_exempt, name='dispatch')
def pilots_import(request: HttpRequest):
    if request.method == 'POST':
        Pilot.objects.all().delete()
        body = request.FILES["file"].read()
        pilots_dict = simplexml.loads(body)['pilots']
        for p in pilots_dict:
            pilot = Pilot(firstname=p['firstname'], lastname=p['lastname'], starting_date=p['starting_date'])
            pilot.save()
        return HttpResponse(status=204)


@method_decorator(csrf_exempt, name='dispatch')
def pilots_remove(request: HttpRequest, id):
    if request.method == 'DELETE':
        pilot = Pilot.objects.get(id=id)
        pilot.delete()
        return HttpResponse(status=204)

@method_decorator(csrf_exempt, name='dispatch')
def airports(request: HttpRequest):
    if request.method == 'GET':
        airports = list(Airport.objects.all().values())
        return JsonResponse(airports, safe=False, encoder=Encoder)

def airports_search(request: HttpRequest):
    if request.method == 'GET':
        with connect() as connection:
            repository = Airports(connection)
            name = request.GET.get('name')
            code = request.GET.get('code')
            city = request.GET.get('city')
            airports = list(Airport.objects.filter(name__icontains=name, code__icontains=code, city__icontains=city).values())
        return JsonResponse(airports, safe=False, encoder=Encoder)

@method_decorator(csrf_exempt, name='dispatch')
def airports_remove(request: HttpRequest, id):
    if request.method == 'DELETE':
        airport = Airport.objects.get(id=id)
        airport.delete()
        return HttpResponse(status=204)

def airports_export(request: HttpRequest):
    airports = list(Airport.objects.all().values())
    return export(request, airports, 'airports')

@method_decorator(csrf_exempt, name='dispatch')
def airports_import(request: HttpRequest):
    if request.method == 'POST':
        Airport.objects.all().delete()
        body = request.FILES["file"].read()
        airports_dict = simplexml.loads(body)['airports']
        for a in airports_dict:
            airport = Airport(name=a['name'], code=a['code'], city=a['city'])
            airport.save()
        return HttpResponse(status=204)

@method_decorator(csrf_exempt, name='dispatch')
def airplanes(request: HttpRequest):
    if request.method == 'GET':
        airplanes = list(Airplane.objects.all().values())
        return JsonResponse(airplanes, safe=False, encoder=Encoder)

@method_decorator(csrf_exempt, name='dispatch')
def airplanes_remove(request: HttpRequest, id):
    if request.method == 'DELETE':
        airplane = Airplane.objects.get(id=id)
        airplane.delete()
        return HttpResponse(status=204)


def airplanes_search(request: HttpRequest):
    if request.method == 'GET':
        build_start = request.GET.get('buildrangeStart')
        build_end = request.GET.get('buildrangeEnd')
        model_name = request.GET.get('modelname')
        airplanes = list(Airplane.objects.filter(model_name__icontains=model_name, build_start__gte=build_start, build_end__lte=build_end).values())
        return JsonResponse(airplanes, safe=False, encoder=Encoder)


def airplanes_export(request: HttpRequest):
    airplanes = Airplane.objects.all()
    return export(request, airplanes, 'airplanes')

@method_decorator(csrf_exempt, name='dispatch')
def airplanes_import(request: HttpRequest):
    if request.method == 'POST':
        Airplane.objects.all().delete()
        body = request.FILES["file"].read()
        airplanes_dict = simplexml.loads(body)['airplanes']
        for a in airplanes_dict:
            airplane = Airplane(modelname=a['modelname'], builddate=a['builddate'])
            airplane.save()
        return HttpResponse(status=204)

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

    mapped_flight = Flight(pilot_id=pilot_id, airplane_id=air_id, departure_airport_id=dep_airp_id, arrival_airport_id=arr_airp_id, departure_time=dep_time, arrival_time=arr_time)
    return mapped_flight

@method_decorator(csrf_exempt, name='dispatch')
def flights(request: HttpRequest):
    if request.method == 'GET':
        flights = list(Flight.objects.all().values())
        return JsonResponse(flights, safe=False, encoder=Encoder)
    elif request.method == 'POST':
        try:
            flight = __map_body_to_flight(request)
        except TypeError as e:
            print(e)
            return HttpResponse(status=400)
        flight.save()
        return HttpResponse(status=200)

@method_decorator(csrf_exempt, name='dispatch')
def flights_update(request: HttpRequest, id):
    if request.method == 'PUT':
        try:
            flight = __map_body_to_flight(request)
            flight.id = id
        except TypeError as e:
            print(e)
            return HttpResponse(status=400)
        flight.save()
        return HttpResponse(status=200)
    if request.method == 'DELETE':
        flight = Flight.objects.get(id=id)
        flight.delete()
        return HttpResponse(status=200)