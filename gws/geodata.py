from gws.models import Restaurant, SkiLift, Slope
from django.core.serializers import serialize


def get_all_restaurants():
    str_geojson = serialize(
        'geojson',
        Restaurant.objects.all(),
        geometry_field='position',
        fields=('id', 'name', 'capacity')
    )

    return str_geojson


def get_all_skilifts():
    str_geojson = serialize(
        'geojson',
        SkiLift.objects.all(),
        geometry_field='track',
        fields=('id', 'name', 'hourly_flow')
    )

    return str_geojson


def get_all_slopes():
    str_geojson = serialize(
        'geojson',
        Slope.objects.all(),
        geometry_field='area',
        fields=('id', 'name', 'color', 'open')
    )

    return str_geojson


def get_restaurant_by_id(restaurant_id):
    str_geojson = serialize(
        'geojson',
        Restaurant.objects.filter(id=restaurant_id),
        geometry_field='position',
        fields=('id', 'name', 'capacity')
    )

    return str_geojson


def get_skilift_by_id(skilift_id):
    str_geojson = serialize(
        'geojson',
        SkiLift.objects.filter(id=skilift_id),
        geometry_field='track',
        fields=('id', 'name', 'hourly_flow')
    )

    return str_geojson


def get_slope_by_id(slope_id):
    str_geojson = serialize(
        'geojson',
        Slope.objects.filter(id=slope_id),
        geometry_field='area',
        fields=('id', 'name', 'color', 'open')
    )

    return str_geojson
