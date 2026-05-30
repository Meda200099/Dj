from django.contrib import admin

from .models import Task, Profile, Appointment

admin.site.register(Task)
admin.site.register(Profile)
admin.site.register(Appointment)
# Register your models here.
