import rasterio
import os


def get_temperature_from_week_and_geolocation(lat, lng, week):

    # opening the geotif image using rasterio
    dataset = rasterio.open('Raster/T' + str(week) + '_image.tif')

    # there is only one band for each image
    band_one = dataset.read(1)

    # link the spatial reference to the columns and rows
    row, col = dataset.index(lng, lat)

    if 0 < row < len(band_one) and 0 < col <len(band_one[0]):
        # return the value (temperature) associated to a specific box in the list
        return band_one[row, col].tolist()

    return None




def all_weeks_temperature(lat, lng):
    arr_temp = []
    nb_rasters = len(os.listdir('Raster'))

    # get all the temperatures for a single location for the whole 7 weeks
    for index in range(0, nb_rasters):
        arr_temp.append(get_temperature_from_week_and_geolocation(lat, lng, index + 1))

    return arr_temp
