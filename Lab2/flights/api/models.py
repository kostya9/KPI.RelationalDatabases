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
