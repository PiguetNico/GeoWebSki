from gws.models import Restaurant, SkiLift, Slope, StoppingPlace
from django.core.serializers import serialize


def objects_to_geojson(objects, geo_field, other_fields):
    str_geojson = serialize(
        'geojson',
        objects,
        geometry_field=geo_field,
        fields=other_fields
    )

    return str_geojson


def restaurants_geojson(objects):
    return objects_to_geojson(
        objects,
        geo_field='position',
        other_fields=('id', 'name', 'capacity')
    )


def skilifts_geojson(objects):
    return objects_to_geojson(
        objects,
        geo_field='track',
        other_fields=('id', 'name', 'hourly_flow')
    )


def slopes_geojson(objects):
    return objects_to_geojson(
        objects,
        geo_field='area',
        other_fields=('id', 'name', 'color', 'open')
    )


def stopping_places_geojson(objects):
    return objects_to_geojson(
        objects,
        geo_field='area',
        other_fields=('id', 'altitude')
    )


def restaurants():
    return restaurants_geojson(Restaurant.objects.all())


def restaurant_by_id(_id):
    return restaurants_geojson(Restaurant.objects.filter(id=_id))


def skilifts():
    return skilifts_geojson(SkiLift.objects.all())


def skilift_by_id(_id):
    return skilifts_geojson(SkiLift.objects.filter(id=_id))


def slopes():
    return slopes_geojson(Slope.objects.all())


def slope_by_id(_id):
    return slopes_geojson(Slope.objects.filter(id=_id))


def stopping_places():
    return stopping_places_geojson(StoppingPlace.objects.all())


def stopping_places_by_id(_id):
    return stopping_places_geojson(StoppingPlace.objects.filter(id=_id))
