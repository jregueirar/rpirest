from django.contrib import admin
from .models import AttachedDevices

# Register your models here.
class AttachedDevicesAdmin(admin.ModelAdmin):
    list_display = ('type', 'name')

admin.site.register(AttachedDevices, AttachedDevicesAdmin)
