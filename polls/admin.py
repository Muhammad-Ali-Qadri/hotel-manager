from django.contrib import admin
from .models import *
from django import forms
# Register your models here.

admin.site.register(Type)
admin.site.register(Profile)
admin.site.register(Images)
admin.site.register(Registration)
admin.site.register(RegistrationDetails)
admin.site.register(Review)


# admin class for defining room interface
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type')
    pass