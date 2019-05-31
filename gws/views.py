from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from . import geodata
from django.views.decorators.csrf import csrf_exempt
from gws.models import Slope
from django.contrib.gis.geos.point import Point
import requests  # used to call the elevation webservice


def index(request):
    api_urls = {
        'foo': 42,
        'restaurants_geojson': reverse('restaurants_geojson'),
        'slopes_geojson': reverse('slopes_geojson'),
        'stoppingplaces_geojson': reverse('stoppingplaces_geojson'),
        'skilifts_geojson': reverse('skilifts_geojson'),
        'route_change_pos': reverse('route_change_pos')
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


# CSRF protection disabled for convenience
@csrf_exempt
def route_change_pos( request ):

    lat = float(request.POST.get('lat'))
    lng = float(request.POST.get('lng'))

    found_slope = find_slope(lat, lng)
    elevation = get_elevation(lat, lng)

    return JsonResponse({
        'slope_id': found_slope.id,
        'slope_name': found_slope.name,
        'elevation': elevation
    })


# Returns the elevation of the position using a webservice
def get_elevation(lat, lng):

    extent_offset = 0.0075  # empirical value to get a good precision
    map_extent = str(lng - extent_offset) + ',' + str(lat - extent_offset)
    map_extent += str(lng + extent_offset) + ',' + str(lat + extent_offset)

    # URL to the elevation webservice of the Copernicus program (European Union)
    elevation_ws_url = 'https://image.discomap.eea.europa.eu/arcgis/rest/services'
    elevation_ws_url += '/Elevation/EUElev_DEM_V11/MapServer/identify'

    parameters = {
        'geometry': str(lng) + ',' + str(lat),  # point coordinates
        'geometryType': 'esriGeometryPoint',  # a Point is sent to the webservice
        'sr': '4326',  # standard CRS for latitudes and longitudes is used
        'tolerance': '3',  # a 3 pixel tolerance is enough
        'mapExtent': map_extent,
        'imageDisplay': '300,300,96',  # width, height and DPI of the elevation map
        'returnGeometry': 'false',  # returning the geometry is useless
        'f': 'json'  # response format in JSON
    }

    r = requests.get(elevation_ws_url, params=parameters)

    try:
        return r.json()['results'][0]['attributes']['Pixel Value'];
    except:
        return None;


def get_neighbour_slopes(current_slope, current_position):

    slopes = Slope.objects.all()


    # a slope can be reached if it intersects lower than the current position

    # a ski lift can be reached if it intersects lower than the current position



def find_slope(lat, lng):

    current_position = Point(
        lng, lat,  # careful! latitude and longitude MUST be reversed here!
        srid=4326  # 4326 used by Leaflet when working with latitude and longitude
    )

    slopes = Slope.objects.all()
    found_slope = None

    # Trying to see if the position is on a slope
    for slope in slopes:
        if slope.area.covers(current_position):
            found_slope = slope

    # If it is not, we consider it belongs to the closest slope
    if found_slope is None:

        min_distance = slopes[0].area.distance(current_position)
        closest_slope = slopes[0]

        # Looking for the slope closest to the provided position
        for slope in slopes[1:]:
            if slope.area.distance(current_position) < min_distance:
                min_distance = slope.area.distance(current_position)
                closest_slope = slope

        found_slope = closest_slope

    return found_slope
