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
from datetime import datetime

from utils import web_tools


class WebTools(unittest.TestCase):
    def setUp(self):

        self.known_scene_l5 = 'LT50370272007121PAC01'
        self.bad_scene5 = 'LT50370272007122PAC01'
        self.known_scene_l7 = 'LE70370272007129EDC00'
        self.bad_scene7 = 'LE70370272007122EDC00'
        self.known_scene_l8 = 'LC80370272014124LGN01'
        self.bad_scene8 = 'LC80370272014122LGN01'
        # known overpasses for pr 37, 27
        self.path_row = 37, 27
        self.overpass_l5 = datetime(2007, 5, 17)
        self.overpass_l7 = datetime(2007, 5, 25)
        self.overpass_l8 = datetime(2014, 5, 20)
        self.search_start = datetime(2007, 5, 16)
        # known centroid of pr 37, 27
        self.latlon = 47.45, -107.951

    def tearDown(self):
        pass

    def test_verify_landsat_scene(self):
        self.assertNotEqual(web_tools.verify_landsat_scene_exists(self.known_scene_l5),
                            web_tools.verify_landsat_scene_exists(self.bad_scene5))
        self.assertNotEqual(web_tools.verify_landsat_scene_exists(self.known_scene_l7),
                            web_tools.verify_landsat_scene_exists(self.bad_scene7))
        self.assertNotEqual(web_tools.verify_landsat_scene_exists(self.known_scene_l8),
                            web_tools.verify_landsat_scene_exists(self.bad_scene8))

        self.assertTrue(web_tools.verify_landsat_scene_exists(self.known_scene_l5))
        self.assertTrue(web_tools.verify_landsat_scene_exists(self.known_scene_l7))
        self.assertTrue(web_tools.verify_landsat_scene_exists(self.known_scene_l8))

    def test_l5_overpass_get(self):
        expect = web_tools.get_l5_overpass_data(self.path_row, self.search_start)
        known = self.overpass_l5
        self.assertEqual((known.year, known.month, known.day),
                         (expect.year, expect.month, expect.day))

    def test_landsat_overpass_time(self):
        sats = ['LT5', 'LE7', 'LC8']
        knowns = [self.overpass_l5, self.overpass_l7, self.overpass_l8]
        for sat, known in zip(sats, knowns):
            if sat == 'LC8':
                start = datetime(2014, 5, 16)
            else:
                start = self.search_start

            expect = web_tools.landsat_overpass_time(self.path_row, start, sat)
            self.assertEqual((known.year, known.month, known.day),
                             (expect.year, expect.month, expect.day))

    def test_wrs2_latlon_convert(self):
        expect_latlon = web_tools.lat_lon_wrs2pr_convert(self.path_row, conversion_type='convert_pr_to_ll')
        self.assertEqual(self.latlon, expect_latlon)

        expect_pr = web_tools.lat_lon_wrs2pr_convert(self.latlon)
        self.assertEqual(self.path_row, expect_pr)


if __name__ == '__main__':
    unittest.main()

# ==================================================================================
