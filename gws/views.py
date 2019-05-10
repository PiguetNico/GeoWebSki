from django.http import HttpResponse
from django.shortcuts import render
from gws import geodata


def index(request):
    return HttpResponse("Hello ! :)")


def request_val(request, identifier):

    if identifier in request.GET:
        return request.GET
    elif identifier in request.POST:
        return request.POST
    else:
        return None


def geodata_restaurants(request):

    restaurant_id = request_val(request, 'id')

    if id in request.GET:
        restaurant_id = request.GET
    elif id in request.POST:
        restaurant_id = request.POST


    if id is None:
        geojson = geodata.get_restaurant_by_id(restaurant_id)
    else:
        geojson = geodata.get_all_restaurants()

    return HttpResponse(geojson, content_type='application/json')


def skimap(request):

    return render(request, 'test.html', {'foo': 42})
