from django.contrib import admin
from .models import Resource, Availability, Booking

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource_type', 'capacity')
    list_filter = ('resource_type',)
    search_fields = ('name',)

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('resource', 'get_day_of_week_display', 'start_time', 'end_time')
    list_filter = ('resource', 'day_of_week')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('resource', 'user', 'start_time', 'end_time', 'is_cancelled')
    list_filter = ('resource', 'is_cancelled', 'start_time')
    search_fields = ('user__username', 'resource__name')
