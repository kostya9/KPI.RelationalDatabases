from django.db import models
from json import JSONEncoder
from django.core.serializers.json import DjangoJSONEncoder
import datetime

# Create your models here.


class Encoder(DjangoJSONEncoder):
        def default(self, value):
            if isinstance(value, datetime.date):
                return DjangoJSONEncoder.default(self, value)
            else:
                return value.__dict__

class Pilot:
    def __init__(self, id, firstname, lastname, starting_date):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.starting_date = starting_date

class Airplane:
    def __init__(self, id, modelname, builddate):
        self.id = id
        self.modelname = modelname
        self.builddate = builddate

class Airport:
    def __init__(self, id, name, code, city):
        self.id = id
        self.name = name
        self.code = code
        self.city = city

class Flight:
    def __init__(self, id, pilot_id, airplane_id, departure_airport_id, arrival_airport_id, departure_time, arrival_time):
        self.id = id
        self.pilot_id = pilot_id
        self.airplane_id = airplane_id
        self.departure_airport_id = departure_airport_id
        self.arrival_airport_id = arrival_airport_id
        self.departure_time = departure_time
        self.arrival_time = arrival_time