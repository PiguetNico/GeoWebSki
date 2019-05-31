from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='homepage'),

    path('route_change_pos', views.route_change_pos, name='route_change_pos'),

    path('geodata/restaurants', views.geodata_restaurants, name='restaurants_geojson'),
    path('geodata/restaurant/<int:_id>', views.geodata_restaurants, name='restaurant_id_geojson'),

    path('geodata/ski-lifts', views.geodata_skilifts, name='skilifts_geojson'),
    path('geodata/ski-lift/<int:_id>', views.geodata_skilifts, name='skilift_id_geojson'),

    path('geodata/slopes', views.geodata_slopes, name='slopes_geojson'),
    path('geodata/slope/<int:_id>', views.geodata_slopes, name='slope_id_geojson'),

    path('geodata/stopping-places', views.geodata_stopping_places, name='stoppingplaces_geojson'),
    path('geodata/stopping-place/<int:_id>', views.geodata_stopping_places, name='stopping_place_id_geojson'),

]