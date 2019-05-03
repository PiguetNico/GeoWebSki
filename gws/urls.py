from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('geo/restaurants', views.geo_restaurants, name='geo_restaurants'),
    path('skimap', views.skimap, name='skimap'),
]