"""
This module downloads landsat data.  Get the wrs (ascending)
from http://landsat.usgs.gov/worldwide_reference_system_WRS.php
select an area you want images for, save the selection and
pass shapefile to this program,
or just choose location coordinates
"""
from landsat.image import Simple
from landsat.downloader import Downloader
from landsat.downloader import RemoteFileDoesntExist
from landsat.search import Search
from os.path import join
from osgeo import ogr
import os
import requests.packages.urllib3
from datetime import datetime


from vector_tools import lat_lon_to_ogr_point, get_path_row

requests.packages.urllib3.disable_warnings()


def download_landsat(start_end_tuple, path_row_tuple=None, lat_lon_tuple=None, shape=None, output_path=None,
                     dry_run=False, max_cloud=None, return_scenes=10):
    start_date, end_date = start_end_tuple[0], start_end_tuple[1]
    path, row = path_row_tuple[0], path_row_tuple[1]

    if shape:
        # assumes shapefile has a 'path' and a 'row' field
        shp_filename = shape
        ds = ogr.Open(shape)
        lyr = ds.GetLayer()
        image_index = [get_path_row(lyr)]
        assert type(image_index) == list
        print 'Downloading landsat by row/path shapefile: {}'.format(shape)

    elif lat and lon:
        point = lat_lon_to_ogr_point(lat, lon)
        print point
        image_index = get_path_row(point, shape)
        assert type(image_index) == list
        print 'Downloading landsat by lat/lon: {}'.format(lat, lon)

    elif path and row:
        image_index = [(path, row)]
        print 'Downloading landsat by path/row: {}, {}'.format(path, row)
        assert type(image_index) == list
    else:
        raise NotImplementedError('Must give path/row tuple, lat/lon tuple plus row/path \n'
                                  'shapefile, or a path/rows shapefile!')

    return_scenes = 100
    if max_cloud:
        max_cloud_percent = 20

    for tile in image_index:
        path, row = tile[0], tile[1]
        searcher = Search()
        destination_path = 'd_{}_{}'.format(path, row)
        os.chdir(output_path)
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        # if os.listdir(destination_path) == []:
        if os.listdir(destination_path):
            print
        print '{} is empty'.format(destination_path)

        downer = Downloader(verbose=False, download_dir='{}\\{}'.format(output_path, destination_path))

        candidate_scenes = searcher.search(paths_rows='{},{},{},{}'.format(path, row, path, row),
                                           start_date=start_date,
                                           end_date=end_date,
                                           cloud_min=0,
                                           cloud_max=max_cloud_percent,
                                           limit=return_scenes)

        print 'total images for tile {} is {}'.format(tile, candidate_scenes['total_returned'])
        if dry_run:
            break
        x = 0
        if candidate_scenes['status'] == 'SUCCESS':
            for scene_image in candidate_scenes['results']:
                print 'Downloading:', (str(scene_image['sceneID']))
                print 'Downloading tile {} of {}'.format(x, candidate_scenes['total_returned'])
                try:
                    downer.download([str(scene_image['sceneID'])])
                    Simple(
                        join('{}\\{}'.format(output_path, destination_path), str(scene_image['sceneID']) + '.tar.bz'))
                    x += 1
                except RemoteFileDoesntExist:
                    print 'Skipping:', (str(scene_image['sceneID']))

        else:
            print 'nothing'

    print 'done'


if __name__ == '__main__':
    home = os.path.expanduser('~')
    print 'home: {}'.format(home)
    start = datetime(2012, 5, 1)
    end = datetime(2012, 9, 30)
    shape = os.path.join(home, 'images', 'vector', 'MT_SPCS_vector', 'US_MJ_tile.shp')
    lat, lon = 47.4, -109.5
    path_int, row_int = 38, 27
    download_landsat((start, end), (lat, lon), dry_run=True)

    # ===============================================================================