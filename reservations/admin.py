from django.contrib import admin
from .models import Resource, Availability, Booking

admin.site.register(Resource)
admin.site.register(Availability)
admin.site.register(Booking)
