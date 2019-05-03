# from django.shortcuts import render
from django.http import HttpResponse
from gws.models import Restaurant
from django.core.serializers import serialize
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello ! :)")


def geo_restaurants(request):
    geojson = serialize(
        'geojson',
        Restaurant.objects.all(),
        geometry_field='position',
        fields=('id', 'name', 'capacity')
    )

    return HttpResponse(geojson, content_type='application/json')


def skimap(request):

    return render(request, 'test.html', {'foo': 42})
