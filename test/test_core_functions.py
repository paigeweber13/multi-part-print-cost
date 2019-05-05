import os
import unittest

import multipartprintpy.core as mpp

"""
assumes that you are running tests from the root of the project directory
"""
class TestCoreFunctions(unittest.TestCase):
    def test_slice_single_model(self):
        try:
            os.remove('test/models/bulbasaur-0.2mm.gcode')
        except FileNotFoundError:
            pass

        expected_command = [
            'bin/slic3r-pe.AppImage', '--slice', '--load',
            'profiles/slic3r-pe-config.ini', '--first-layer-height', '0.25',
            '--layer-height', '0.2', 'test/models/bulbasaur.stl',
            '--output', 'test/models/bulbasaur-0.2mm.gcode'
            ]
        self.assertEqual(expected_command, mpp.slice_model(0.2, 0, 'test/'
            + 'models/bulbasaur.stl'))
        self.assertTrue(os.path.isfile('test/models/bulbasaur-0.2mm.gcode'))

    def test_scrape_time_and_usage_estimates_from_gcode(self):
        expected_result = 'filament used: 4.01m\n' \
                        + '               9.6cm3\n' \
                        + '               12.0g\n' \
                        + 'filament cost: 0.2 USD\n' \
                        + 'estimated print time: 52m28s\n'
        actual_result = mpp.scrape_time_and_usage_estimates(
            ['bulbasaur-0.2mm.gcode'])
        self.assertEqual(expected_result, actual_result)
