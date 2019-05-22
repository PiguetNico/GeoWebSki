from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='homepage'),

    path('geodata/restaurants', views.geodata_restaurants, name='restaurants_json'),
    path('geodata/restaurant/<int:_id>', views.geodata_restaurants, name='restaurant_id_json'),

    path('geodata/ski-lifts', views.geodata_skilifts, name='skilifts_json'),
    path('geodata/ski-lift/<int:_id>', views.geodata_skilifts, name='skilift_id_json'),

    path('geodata/slopes', views.geodata_slopes, name='slopes_json'),
    path('geodata/slope/<int:_id>', views.geodata_slopes, name='slope_id_json'),

    path('geodata/stopping-places', views.geodata_stopping_places, name='stopping_places_json'),
    path('geodata/stopping-place/<int:_id>', views.geodata_stopping_places, name='stopping_place_id_json'),

]