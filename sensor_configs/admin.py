from django.contrib import admin
from sensor_configs import models

# Register your models here.
admin.site.register(models.Sensor, admin.ModelAdmin)
admin.site.register(models.Watertype, admin.ModelAdmin)