# from django.contrib import admin
from django.contrib.gis import admin

# Registering our models
from .models import Slope, SkiLift, Restaurant, StoppingPlace

# (use "admin.GeoModelAdmin" to use Open Layers maps)
# (use "admin.OSMGeoAdmin" to use OpenStreetMaps maps)

admin.site.register(Slope, admin.OSMGeoAdmin)
admin.site.register(SkiLift, admin.OSMGeoAdmin)
admin.site.register(Restaurant, admin.OSMGeoAdmin)
admin.site.register(StoppingPlace, admin.OSMGeoAdmin)
