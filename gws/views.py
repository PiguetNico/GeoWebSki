from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from . import geodata
from . import weather_points
from . import ski_resort_routing as gws_routing
from django.views.decorators.csrf import csrf_exempt
from gws.models import Slope, SkiLift, StoppingPlace, Restaurant


def index(request):
    api_urls = {
        'foo': 42,
        'restaurants_geojson': reverse('restaurants_geojson'),
        'slopes_geojson': reverse('slopes_geojson'),
        'stoppingplaces_geojson': reverse('stoppingplaces_geojson'),
        'skilifts_geojson': reverse('skilifts_geojson'),
        'route_change_pos': reverse('route_change_pos'),
        'temperature_geojson': reverse('temperature_geojson')
    }
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


# CSRF protection disabled for convenience
@csrf_exempt
def weather_points_all_weeks_temperature(request):

    lat = float(request.POST.get('lat'))
    lng = float(request.POST.get('lng'))

    if lat is not None and lng is not None:
        temp = weather_points.all_weeks_temperature(lat, lng)
    else:
        temp = None

    return JsonResponse({
        'temperatures': temp
    })


# CSRF protection disabled for convenience
@csrf_exempt
def route_change_pos(request):

    lat = float(request.POST.get('lat'))
    lng = float(request.POST.get('lng'))
    restaurant_id = float(request.POST.get('restaurant_id'))

    current_place = gws_routing.find_stoppingplace(lat, lng)
    elevation = gws_routing.get_elevation(lat, lng)

    # Selecting a random Restaurant
    restaurant = Restaurant.objects.filter(id=restaurant_id)[0]
    restaurant_point = restaurant.position.transform(4326, clone=True)
    restaurant_place = gws_routing.find_stoppingplace(restaurant_point.y, restaurant_point.x)

    route = gws_routing.get_ski_route(current_place, restaurant_place)

    return JsonResponse({
        'elevation': elevation,
        'route': route
    })
