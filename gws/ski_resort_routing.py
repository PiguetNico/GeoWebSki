from gws.models import Restaurant, SkiLift, Slope, StoppingPlace
import geopandas as gpd


def asdf():

    slopes = Slope.objects.all()
    slopes.tostring()
