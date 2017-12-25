from django.db import models
from json import JSONEncoder
from django.core.serializers.json import DjangoJSONEncoder
import datetime

# Create your models here.


class Encoder(DjangoJSONEncoder):
        def default(self, value):
            if isinstance(value, datetime.date):
                return DjangoJSONEncoder.default(self, value)

class Pilot(models.Model):
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)
    starting_date = models.DateField()

class Airplane(models.Model):
    modelname = models.CharField(max_length=60)
    builddate = models.DateField()


class Airport(models.Model):
    name = models.CharField(max_length=60)
    code = models.CharField(max_length=60)
    city = models.CharField(max_length=60)

class Flight(models.Model):
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='+')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='+')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()