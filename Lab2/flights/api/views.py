from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from api.repositories.pilots import Pilots
import MySQLdb
from api.models import Encoder, Pilot
import json

def connect():
    return MySQLdb.connect(host="localhost",
                     user="root",
                     db="flights")

# Create your views here.
def index(request: HttpRequest):
    if request.method == 'GET':
        return JsonResponse({'text': '123'})

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
            firstname = pilot["firstname"]
            lastname = pilot["lastname"]
            start_date = pilot["starting_date"]
            pilot = Pilot(0, firstname, lastname, start_date)
        except TypeError:
            return HttpResponse(status=400)
        with connect() as connection:
            repository = Pilots(connection)
            repository.add(pilot)
        return HttpResponse(status=200)


def airports(reqiest: HttpRequest):
    raise Error()

def airplanes(reqiest: HttpRequest):
    raise Error()