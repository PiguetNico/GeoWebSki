from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from . import geodata
from . import weather_points
from django.views.decorators.csrf import csrf_exempt
from gws.models import Slope, SkiLift, StoppingPlace, Restaurant
from django.contrib.gis.geos.point import Point
import requests  # used to call the elevation webservice
import networkx as nx
from networkx.exception import NetworkXNoPath, NodeNotFound


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

    current_place = find_stoppingplace(lat, lng)
    elevation = get_elevation(lat, lng)

    # Selecting a random Restaurant
    restaurant = Restaurant.objects.filter(id=restaurant_id)[0]
    restaurant_point = restaurant.position.transform(4326, clone=True)
    restaurant_place = find_stoppingplace(restaurant_point.y, restaurant_point.x)

    route = get_ski_route(current_place, restaurant_place)

    return JsonResponse({
        'elevation': elevation,
        'route': route
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


def get_ski_route(start_place, end_place):
    graph = generate_directed_graph()

    try:
        sp = nx.shortest_path(graph, start_place, end_place)

        route = list()

        for i in range(0,len(sp)-1):

            edge_obj = graph.edges[sp[i], sp[i+1]]['obj']
            edge_type = 'unknown'

            if isinstance(edge_obj, Slope):
                edge_type = 'slope'
            if isinstance(edge_obj, SkiLift):
                edge_type = 'skilift'

            from_point = sp[i].area.centroid.transform(4326, clone=True)
            to_point = sp[i+1].area.centroid.transform(4326, clone=True)

            route.append({
                'from': {
                    'id': sp[i].id,
                    'location': {
                        'lat': from_point.y,
                        'lng': from_point.x
                    }
                },
                'through': {
                    'id': edge_obj.id,
                    'type': edge_type,
                    'name': str(edge_obj)
                },
                'to': {
                    'id': sp[i+1].id,
                    'location': {
                        'lat': to_point.y,
                        'lng': to_point.x
                    }
                }
            })

        return route

    except (NetworkXNoPath, NodeNotFound):
        return False



def generate_directed_graph():

    # vertices are StoppingPlace objects
    # edges are Slope or SkiLift objects
    all_stoppingplaces = list(StoppingPlace.objects.all())

    graph = nx.DiGraph()
    ia = 1  # this avoids testing the same pair of nodes twice

    for a in all_stoppingplaces[:-1]:
        a_neighbours = get_stoppingplace_neighbours(a)

        for b in all_stoppingplaces[ia:]:
            b_neighbours = get_stoppingplace_neighbours(b)

            common_neighbours = a_neighbours & b_neighbours

            if len(common_neighbours) > 0:
                a_elevation = pt_elevation(a.area.centroid)
                b_elevation = pt_elevation(b.area.centroid)

                for cn in common_neighbours:
                    if isinstance(cn, Slope) and cn.open:
                        if a_elevation >= b_elevation:
                            # insert link from a to b through cn
                            graph.add_edge(a, b, obj=cn)

                        else:
                            # insert link from b to a through cn
                            graph.add_edge(b, a, obj=cn)

                    elif isinstance(cn, SkiLift) and cn.open:
                        if a_elevation < b_elevation:
                            # insert link from a to b through cn
                            graph.add_edge(a, b, obj=cn)

                        if a_elevation > b_elevation and cn.twoways:
                            # insert link from b to a through cn
                            graph.add_edge(b, a, obj=cn)
        ia += 1
    return graph


def get_stoppingplace_neighbours(stoppingplace):

    all_slopes = list(Slope.objects.all())
    all_skilifts = list(SkiLift.objects.all())
    neighbours = set()

    for slope in all_slopes:
        if not stoppingplace.area.intersection(slope.area).empty:
            neighbours.add(slope)

    for skilift in all_skilifts:
        if not stoppingplace.area.intersection(skilift.track).empty:
            neighbours.add(skilift)

    return neighbours


def find_stoppingplace(lat, lng):

    current_position = Point(
        lng, lat,  # careful! latitude and longitude MUST be reversed here!
        srid=4326  # 4326 used by Leaflet when working with latitude and longitude
    )

    places = StoppingPlace.objects.all()
    found_place = None

    # Trying to see if the position is on a slope
    for place in places:
        if current_position.within(place.area):
            found_place = place

    # If it is not, we consider it belongs to the closest slope
    if found_place is None:

        min_distance = places[0].area.distance(current_position)
        closest_place = places[0]

        # Looking for the slope closest to the provided position
        for place in places[1:]:
            if current_position.distance(place.area) < min_distance:
                min_distance = current_position.distance(place.area)
                closest_place = place

        found_place = closest_place

    return found_place
