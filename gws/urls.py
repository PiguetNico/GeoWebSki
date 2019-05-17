from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ski-map', views.ski_map, name='ski_map'),

    path('geodata/restaurants', views.geodata_restaurants, name='geodata_restaurants_all'),
    path('geodata/restaurant/<int:_id>', views.geodata_restaurants, name='geodata_restaurant_id'),

    path('geodata/ski-lifts', views.geodata_skilifts, name='geodata_skilifts_all'),
    path('geodata/ski-lift/<int:_id>', views.geodata_skilifts, name='geodata_skilift_id'),

    path('geodata/stopping-places', views.geodata_stopping_places, name='geodata_stopping_places'),
    path('geodata/stopping-place/<int:_id>', views.geodata_stopping_places, name='geodata_stopping_place_id'),

]