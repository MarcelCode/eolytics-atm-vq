from django.contrib import admin
from sensor_configs import models

# Register your models here.
admin.site.register(models.ConfigLandsat8, admin.ModelAdmin)
admin.site.register(models.ConfigSentinel2, admin.ModelAdmin)
admin.site.register(models.Sensor, admin.ModelAdmin)
admin.site.register(models.Watertype, admin.ModelAdmin)