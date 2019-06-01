from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from . import geodata
from django.views.decorators.csrf import csrf_exempt
from gws.models import Slope, SkiLift
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

# Returns the elevation of a Point object
def pt_elevation(point):
    # The point is converted into its SR 4326 equivalent
    point_sr_4326 = point.transform(4326, clone=True)

    # Temporarily storing latitude and longitude (for clarity/readability)
    lat = point_sr_4326.y
    lng = point_sr_4326.x

    return get_elevation(lat, lng)

# Returns the elevation of the position using a webservice.
# Expects SR 4326 latitude and longitude!
def get_elevation(lat, lng):

    extent_offset = 0.0075  # empirical value to get a good precision
    map_extent = str(lng - extent_offset) + ',' + str(lat - extent_offset)
    map_extent += ','
    map_extent += str(lng + extent_offset) + ',' + str(lat + extent_offset)

    # URL to the elevation webservice of the Copernicus program (European Union)
    elevation_ws_url = 'https://image.discomap.eea.europa.eu/arcgis/rest/services'
    elevation_ws_url += '/Elevation/EUElev_DEM_V11/MapServer/identify'

    parameters = {
        'geometry': str(lng) + ',' + str(lat),  # point coordinates
        'geometryType': 'esriGeometryPoint',  # a Point is sent to the webservice
        'sr': '4326',  # Spatial reference 4326 is used by default
        'tolerance': '3',  # a 3 pixel tolerance is enough
        'mapExtent': map_extent,
        'imageDisplay': '300,300,96',  # width, height and DPI of the elevation map
        'returnGeometry': 'false',  # returning the geometry is useless
        'f': 'json'  # response format in JSON
    }

    r = requests.get(elevation_ws_url, params=parameters)

    try:
        return float(r.json()['results'][0]['attributes']['Pixel Value'])
    except:
        return None


def asdf(start_slope, start_position, end_slope):

    current_place = start_slope
    current_pos = start_position

    all_slopes = list(Slope.objects.all())
    all_skilifts = list(SkiLift.objects.all())

    to_visit = list()
    visited = set()

    


def is_slope_reachable(current_place, current_pos, slope):

    # Slope-to-slope connection to check
    if isinstance(current_place, Slope):
        current_slope = current_place
        intersection = current_slope.area.intersection(slope.area)

        # if the current slope does not intersect with the other, we cannot reach it
        if intersection.empty:
            return False
        # if it does intersect, we consider we can reach it if we are higher than the
        # intersection's centroid
        elif pt_elevation(current_pos) > pt_elevation(intersection.centroid):
            return True
        else:
            return False

    # Skilift-to-slope connection to check
    elif isinstance(current_place, SkiLift):
        current_lift = current_place
        lift_start = current_lift.track[0]
        lift_end = current_lift.track[-1]

        start_intersect = lift_start.intersection(slope.area)
        end_intersect = lift_end.intersection(slope.area)

        if not end_intersect.empty:
            return True
        elif current_lift.twoways and not start_intersect.empty:
            return True
        else:
            return False
    else:
        return False


def is_skilift_reachable(current_place, current_pos, skilift):

    # it is impossible to reach a skilift from a skilift
    # (...unless your name is James Bond or something.
    # In which case you're probably not there to enjoy ski holidays
    # anyway so thanks for saving the world again and God save the Queen)
    if isinstance(current_place, SkiLift):
        return False

    elif isinstance(current_place, Slope):
        current_slope = current_place
        lift_start = skilift.track[0]
        lift_end = skilift.track[-1]

        start_intersect = current_slope.area.intersection(lift_start)
        end_intersect = current_slope.area.intersection(lift_end)

        # CHECK ELEVATION !!
        if not start_intersect.empty and pt_elevation(current_pos) > pt_elevation(start_intersect):
            return True
        elif not end_intersect.empty and skilift.twoways:
            return True
        else:
            return False
    else:
        return False


def find_slope(lat, lng):

    current_position = Point(
        lng, lat,  # careful! latitude and longitude MUST be reversed here!
        srid=4326  # 4326 used by Leaflet when working with latitude and longitude
    )

    slopes = Slope.objects.all()
    found_slope = None

    # Trying to see if the position is on a slope
    for slope in slopes:
        if current_position.within(slope.area):
            found_slope = slope

    # If it is not, we consider it belongs to the closest slope
    if found_slope is None:

        min_distance = slopes[0].area.distance(current_position)
        closest_slope = slopes[0]

        # Looking for the slope closest to the provided position
        for slope in slopes[1:]:
            if current_position.distance(slope.area) < min_distance:
                min_distance = current_position.distance(slope.area)
                closest_slope = slope

        found_slope = closest_slope

    return found_slope
