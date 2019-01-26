from django.contrib import admin
from projects import models

admin.site.register(models.UserProject, admin.ModelAdmin)
admin.site.register(models.UserSensor, admin.ModelAdmin)
