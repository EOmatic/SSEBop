# ===============================================================================
# Copyright 2017 ross, dgketchum
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

from __future__ import print_function

import os
import sys
from datetime import datetime

import yaml

from app.paths import paths

DEFAULT_CFG = '''
input_root: /path/to/inputs
output_root: /path/to/output

api_key: 'please_set_from_Mapzen'

satellite: LT5
single_date: False
start_date: 12/1/2013
end_date: 12/31/2013
k_factor: 1.25
verify_paths: True

# Add the path relative to /input_root/
# They will be joined to input_root.
polygons: /path/to/please_set_me.shp
mask: /path/to/mask/please_set_me.tif
'''

DATETIME_FMT = '%m/%d/%Y'


class RunSpec:
    _obj = None
    input_root = None
    output_root = None
    api_key = None
    single_date = False
    start_date = None
    end_date = None
    mask = None
    polygons = None
    satellite = None
    k_factor = None
    verify_paths = None

    def __init__(self, obj):
        self._obj = obj
        attrs = ('input_root', 'output_root', 'api_key',
                 'start_date', 'end_date',
                 'mask', 'polygons',
                 'satellite', 'image_directory',
                 'k_factor', 'dem_folder',
                 'tmax_folder', 'dt_folder',
                 'eto_folder', 'verify_paths',)

        for attr in attrs:
            setattr(self, attr, self._obj.get(attr))

    @property
    def save_dates(self):
        sd = self._obj.get('save_dates')
        if sd:
            return [datetime.strptime(s, DATETIME_FMT) for s in sd]

    @property
    def date_range(self):
        obj = self._obj
        if 'start_year' in obj:
            return (datetime(obj['start_year'],
                             obj['start_month'],
                             obj['start_day']),
                    datetime(obj['end_year'],
                             obj['end_month'],
                             obj['end_day']))
        else:
            return (datetime.strptime(obj['start_date'], DATETIME_FMT),
                    datetime.strptime(obj['end_date'], DATETIME_FMT))


class Config:
    runspecs = None

    def __init__(self, path=None):
        self.load(path=path)

    def load(self, path=None):
        if path is None:
            path = paths.config

        if isinstance(path, str):
            check_config(path)
            rfile = open(path, 'r')
        else:
            rfile = path

        self.runspecs = [RunSpec(doc) for doc in yaml.load_all(rfile)]
        rfile.close()


def check_config(path=None):
    if path is None:
        path = paths.config

    if not os.path.isfile(path):
        print('\n***** The config file {} does not exist. A default one will be written'.format(path))

        with open(path, 'w') as wfile:
            print('-------------- DEFAULT CONFIG -----------------')
            print(DEFAULT_CFG)
            print('-----------------------------------------------')
            wfile.write(DEFAULT_CFG)

        print('***** Please edit the config file at {} and run the model *****\n'.format(
            os.path.join(os.getcwd(), path)))

        sys.exit()

# ============= EOF =============================================
