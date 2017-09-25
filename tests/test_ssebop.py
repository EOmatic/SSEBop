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

from app.config import Config
from app.paths import paths

from core.ssebop import SSEBopModel
from core.ssebop import SSEBopGeo

from sat_image.image import Landsat8


class SSEBopModelTestCaseLC8(unittest.TestCase):
    def setUp(self):
        self.config_path = 'tests/ssebop_config_test_lc8.yml'
        self.cfg = Config(self.config_path)

    def test_config(self):
        self.assertIsInstance(self.cfg, Config)

    def test_runspecs(self):
        for runspec in self.cfg.runspecs:
            paths.build(runspec.root)
            self.assertEqual(runspec.k_factor, 1.25)

    def test_instantiate_ssebop(self):
        for runspec in self.cfg.runspecs:
            paths.build(runspec.root)
            sseb = SSEBopModel(runspec)
            self.assertIsInstance(sseb, SSEBopModel)
            sseb.configure_run()
            self.assertTrue(sseb._is_configured, True)
            self.assertEqual(runspec.satellite, sseb.satellite)

    def test_image_geo(self):
        for runspec in self.cfg.runspecs:
            paths.build(runspec.root)

            sseb = SSEBopModel(runspec)
            setattr(sseb, 'image', Landsat8(sseb.image_dir))
            image_geo = SSEBopGeo(sseb.image_id, sseb.image_dir,
                                  sseb.image.get_tile_geometry(),
                                  sseb.image.transform,
                                  sseb.image.profile,
                                  sseb.image.rasterio_geometry,
                                  sseb.image.bounds,
                                  sseb.api_key, sseb.image_date)

            self.assertIsInstance(image_geo, SSEBopGeo)
            self.assertIsInstance(image_geo.image_dir, str)

    def test_cold_pix(self):
        for runspec in self.cfg.runspecs:
            paths.build(runspec.root)
            sseb = SSEBopModel(runspec)
            sseb.configure_run()
            ts = sseb.image.land_surface_temp()
            c = sseb.c_factor(ts)
            self.assertEqual(c, 1.05873032846)

    def test_difference_temp(self):
        for runspec in self.cfg.runspecs:
            paths.build(runspec.root)
            sseb = SSEBopModel(runspec)
            sseb.configure_run()
            dt = sseb.difference_temp()
            self.assertEqual(dt, 300)
if __name__ == '__main__':
    unittest.main()

# ===============================================================================
