from django.contrib import admin

# Register your models here.
from .models import Slope, SkiLift, Restaurant

admin.site.register(Slope)
admin.site.register(SkiLift)
admin.site.register(Restaurant)
