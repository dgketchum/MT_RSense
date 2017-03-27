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
import os
import numpy as np
from netCDF4 import Dataset, num2date
from datetime import datetime, timedelta
from xlrd import xldate



lat_bound = [44, 49]
lon_bound = [-117, -104]


def get_gridmet(day):
    """ get day values frof U of I gridmet, return as numpy array per variable
    :param day:
    :return:

    note: dates are in xl '1900' format, i.e., number of days since 1899-12-31 23:59
    """

    # get dataset from internet
    variables = ['pr', 'rmax', 'rmin', 'sph', 'srad', 'th', 'tmmn', 'tmmx', 'pet', 'vs']
    print 'for year {}'.format(day.year)

    site = 'http://thredds.northwestknowledge.net:8080/thredds/dodsC/MET/pet/pet_{}.nc'.format(day.year)
    nc = Dataset(site)
    print nc.variables.keys()

    date_tup = (day.year, day.month, day.day)
    excel_date = xldate.xldate_from_date_tuple(date_tup, 0)
    print 'excel date from datetime: {}'.format(excel_date)

    time_arr = nc.variables['day'][:]
    date_index = np.argmin(np.abs(time_arr - excel_date))

    # find indices of lat lon bounds in nc file
    lats = nc.variables['lat'][:]
    lons = nc.variables['lon'][:]
    lat_lower = np.argmin(np.abs(lats - lat_bound[1]))
    lat_upper = np.argmin(np.abs(lats - lat_bound[0]))
    lon_lower = np.argmin(np.abs(lons - lon_bound[0]))
    lon_upper = np.argmin(np.abs(lons - lon_bound[1]))

    subset = nc.variables['potential_evapotranspiration'][date_index, :, :]  # lat_lower:lat_upper, lon_lower:lon_upper]
    nc.close()
    print 'variable of type {} has shape {}'.format(type(subset), subset.shape)


if __name__ == '__main__':
    home = os.path.expanduser('~')
    day = datetime(2016, 4, 1, 12)
    get_gridmet(day)

    # ===============================================================================