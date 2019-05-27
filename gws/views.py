from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from . import geodata


def index(request):
    api_urls = {
        'foo': 42,
        'restaurants_geojson': reverse('restaurants_geojson'),
        'slopes_geojson': reverse('slopes_geojson'),
        'stoppingplaces_geojson': reverse('stoppingplaces_geojson'),
        'skilifts_geojson': reverse('skilifts_geojson')
    };
    return render(request, 'map.html', api_urls)


def request_val(request, identifier):
    if identifier in request.GET:
        return request.GET
    elif identifier in request.POST:
        return request.POST
    else:
        return None


def geodata_restaurants(request, _id=None):
    return HttpResponse(
        geodata.restaurant_by_id(_id)
        if (_id is not None)
        else geodata.restaurants(),

        content_type='application/json'
    )


def geodata_skilifts(request, _id=None):
    return HttpResponse(
        geodata.skilift_by_id(_id)
        if (_id is not None)
        else geodata.skilifts(),

        content_type='application/json'
    )


def geodata_slopes(request, _id=None):
    return HttpResponse(
        geodata.slope_by_id(_id)
        if (_id is not None)
        else geodata.slopes(),

        content_type='application/json'
    )


def geodata_stopping_places(request, _id=None):
    return HttpResponse(
        geodata.stopping_places_by_id(_id)
        if (_id is not None)
        else geodata.stopping_places(),

        content_type='application/json'
    )
