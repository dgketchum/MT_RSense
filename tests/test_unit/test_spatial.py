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

import unittest
import pkg_resources

from utils import spatial_reference_tools as srt


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.mtspcs_tif = 'LT05_L1GS_036029_20060523_test_MTSPCS.tif'
        self.wgs_tif = 'LT05_L1GS_036029_20060523_test_WGS84.tif'
        self.wgs_tile_on = pkg_resources.resource_filename('data',
                                                           'wrs2_036029_WGS.shp')
        self.wgs_tile_off = pkg_resources.resource_filename('data',
                                                            'US_MJ_tile_WGS.shp')

    def tearDown(self):
        pass

    def test_shp_srs(self):
        print self.wgs_tile_on
        srs = srt.shp_spatial_reference(self.wgs_tile_on)


if __name__ == '__main__':
    unittest.main()

# ===============================================================================
