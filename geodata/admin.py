from django.contrib.gis import admin
from .models import *

admin.site.register(Country, admin.GeoModelAdmin)
admin.site.register(UserData, admin.GeoModelAdmin)
admin.site.register(UserProjectShape, admin.GeoModelAdmin)