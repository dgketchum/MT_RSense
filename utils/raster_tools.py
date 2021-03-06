# ===============================================================================
# Copyright 2017 dgketchum
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
"""
The purpose of this module is to provide some simple tools needed for raster processing.


"""
import os

from numpy import array, asarray
from numpy.ma import masked_where, nomask
from osgeo import gdal, ogr

import spatial_reference_tools as srt


def raster_to_array(input_raster_path, raster=None, band=1):
    """
    Convert .tif raster into a numpy numerical array.

    :param input_raster_path: Path to raster.
    :param raster: Raster name with *.tif
    :param band: Band of raster sought.
    :return: Numpy array.
    """
    try:
        raster_open = gdal.Open(os.path.join(input_raster_path, raster))
    except TypeError:
        raster_open = gdal.Open(input_raster_path)
    except AttributeError:
        raster_open = gdal.Open(input_raster_path)
    ras = array(raster_open.GetRasterBand(band).ReadAsArray(), dtype=float)
    return ras


def get_polygon_from_raster(raster):
    tile_id = os.path.basename(raster)
    # print 'tile number: {}'.format(tile_id)
    # print 'get poly tile: {}'.format(tile_id)
    # get raster geometry
    tile = gdal.Open(raster)
    # print 'tile is type: {}'.format(tile)
    transform = tile.GetGeoTransform()
    pixel_width = transform[1]
    pixel_height = transform[5]
    cols = tile.RasterXSize
    rows = tile.RasterYSize

    x_left = transform[0]
    y_top = transform[3]
    x_right = x_left + cols * pixel_width
    y_bottom = y_top - rows * pixel_height

    ring = ogr.Geometry(ogr.wkbLinearRing)
    ring.AddPoint(x_left, y_top)
    ring.AddPoint(x_left, y_bottom)
    ring.AddPoint(x_right, y_top)
    ring.AddPoint(x_right, y_bottom)
    ring.AddPoint(x_left, y_top)
    raster_geo = ogr.Geometry(ogr.wkbPolygon)
    raster_geo.AddGeometry(ring)
    # print 'found poly tile geo: {}'.format(raster_geo)
    return raster_geo


def find_poly_ras_intersect(shape, raster_dir, extension='.tif'):
    """  Finds all the tiles falling within raster object
    the get shape geometry should be seperated from the intesect check,
    currently causes a exit code 139 on unix box

    :param polygon:
    :param extension:
    :param raster_dir:
    """

    print 'starting shape: {}'.format(shape)

    # get vector geometry
    if not os.path.isfile(shape):
        raise NotImplementedError('Shapefile not found')
    polygon = ogr.Open(shape)
    layer = polygon.GetLayer()
    feature = layer.GetFeature(0)
    vector_geo = feature.GetGeometryRef()
    # print 'vector geometry: {}'.format(vector_geo)

    tiles = [os.path.join(raster_dir, x) for x in
             os.listdir(os.path.join(raster_dir)) if x.endswith(extension)]

    raster_list = []
    for tile in tiles:
        print tile, srt.tif_proj4_spatial_reference(tile)
        if srt.check_same_reference_system(shape, tile):
            raster_geo = get_polygon_from_raster(tile)
            if raster_geo.Intersect(vector_geo):
                print 'tile: {} intersects {}'.format(os.path.basename(tile), os.path.basename(shape))
                raster_list.append(tile)

    return raster_list


def apply_mask(mask_path, arr):
    out = None
    file_name = next((fn for fn in os.listdir(mask_path) if fn.endswith('.tif')), None)
    if file_name is not None:
        mask = raster_to_array(mask_path, file_name)
        idxs = asarray(mask, dtype=bool)
        out = arr[idxs].flatten()
    return out


def remake_array(mask_path, arr):
    out = None
    file_name = next((filename for filename in os.listdir(mask_path) if filename.endswith('.tif')), None)
    if file_name is not None:
        mask_array = raster_to_array(mask_path, file_name)
        masked_arr = masked_where(mask_array == 0, mask_array)
        masked_arr[~masked_arr.mask] = arr.ravel()
        masked_arr.mask = nomask
        arr = masked_arr.filled(0)
        out = arr

    return out


def array_to_raster(save_array, out_path, geo):
    key = None
    pass
    driver = gdal.GetDriverByName('GTiff')
    out_data_set = driver.Create(out_path, geo['cols'], geo['rows'],
                                 geo['bands'], geo['data_type'])
    out_data_set.SetGeoTransform(geo['geotransform'])
    out_data_set.SetProjection(geo['projection'])
    output_band = out_data_set.GetRasterBand(1)
    output_band.WriteArray(save_array, 0, 0)
    print 'written array {} mean value: {}'.format(key, save_array.mean())

    return None


if __name__ == '__main__':
    pass
    # home = os.path.expanduser('~')
    # terrain = os.path.join(home, 'images', 'terrain', 'ned_tiles', 'dem')
    # shape = os.path.join(home, 'images', 'vector_data', 'wrs2_descending',
    #                      'wrs2_036029_Z12.shp')
    # find_poly_ras_intersect(shape, terrain)

# =================================== EOF =========================
