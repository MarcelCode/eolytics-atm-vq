from django.contrib import admin
from portal import models

# Register your models here.
admin.site.register(models.Sensor)
admin.site.register(models.Products)
admin.site.register(models.RrsConfig)
admin.site.register(models.Landsat8)
admin.site.register(models.Sentinel2)
