from django.contrib import admin

from .models import Manufacturer, Region, Transformer

# Register your models here.
admin.site.register(Manufacturer)
admin.site.register(Region)
admin.site.register(Transformer)
