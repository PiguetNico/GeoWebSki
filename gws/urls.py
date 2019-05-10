from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('geodata/restaurant', views.data_restaurants, name='data_restaurants'),
    path('skimap', views.skimap, name='skimap'),
]