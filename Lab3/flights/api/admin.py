from django.contrib import admin

# Register your models here.

from api.models import Encoder, Pilot, Flight, Airplane, Airport

admin.site.register(Flight)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Pilot)