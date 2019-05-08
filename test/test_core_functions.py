"""
tests core functionality. assumes that you are running tests from the root of
the project directory
"""

import datetime
import os
import unittest

import multipartprintpy.core as mpp

class TestCoreFunctions(unittest.TestCase):
    """
    tests things like slicing models and parsing the time/filament usage data
    """
    def test_slice_single_model(self):
        """
        tries to slice a single model with 0.2mm layer height and checks to see if the file exists. Not a really robust check, but it works
        """
        try:
            os.remove('test/models/bulbasaur-0.2mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [[
            'bin/slic3r-pe.AppImage', '--slice', '--load',
            'profiles/slic3r-pe-config.ini', '--first-layer-height', '0.25',
            '--layer-height', '0.2', 'test/models/bulbasaur.stl',
            '--output', 'test/models/bulbasaur-0.2mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_model(0.2, False, ['test/' +
                                         'models/bulbasaur.stl']))
        self.assertTrue(os.path.isfile('test/models/bulbasaur-0.2mm.gcode'))

        try:
            os.remove('test/models/bulbasaur-0.2mm.gcode')
        except FileNotFoundError:
            pass

    def test_slice_single_model_with_supports(self):
        """
        """
        try:
            os.remove('test/models/support-test-0.1mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [[
            'bin/slic3r-pe.AppImage', '--slice', '--load',
            'profiles/slic3r-pe-config.ini', '--first-layer-height', '0.15',
            '--layer-height', '0.1', 'test/models/support-test.stl', '--support-material', '--output',
            'test/models/support-test-0.1mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_model(0.1, True, ['test/' +
                                         'models/support-test.stl']))
        self.assertTrue(os.path.isfile('test/models/support-test-0.1mm.gcode'))

        try:
            os.remove('test/models/support-test-0.1mm.gcode')
        except FileNotFoundError:
            pass

    def test_slice_large_model(self):
        """
        """
        try:
            os.remove('test/models/large-box-0.3mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [[
            'bin/slic3r-pe.AppImage', '--slice', '--load',
            'profiles/slic3r-pe-config.ini', '--first-layer-height', '0.35',
            '--layer-height', '0.3', 'test/models/large-box.stl', '--support-material', '--output',
            'test/models/large-box-0.3mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_model(0.3, True, ['test/' +
                                         'models/large-box.stl']))
        self.assertTrue(os.path.isfile('test/models/large-box-0.3mm.gcode'))

        try:
            os.remove('test/models/large-box-0.3mm.gcode')
        except FileNotFoundError:
            pass

    def test_scrape_time_and_usage_estimates_from_gcode(self):
        """
        sees if scrape_time function can get the data from a gcode
        """
        expected_result = [{
            'name-of-file': 'test/gcodes/bulbasaur-0.2mm.gcode',
            'filament-used-m': 4.01,
            'filament-used-cm3': 9.6,
            'filament-used-g': 12.0,
            'filament-cost-usd': 0.2,
            'print-time': datetime.timedelta(minutes=52, seconds=28)
        }]
        actual_result = mpp.scrape_time_and_usage_estimates(
            ['test/gcodes/bulbasaur-0.2mm.gcode'])
        self.assertEqual(expected_result, actual_result)

    def test_scrape_time_and_usage_estimates_from_gcode_with_supports(self):
        """
        sees if scrape_time function can get the data from a gcode
        """
        expected_result = [{
            'name-of-file': 'test/gcodes/support-test-0.1mm.gcode',
            'filament-used-m': 2.39,
            'filament-used-cm3': 5.7,
            'filament-used-g': 7.1,
            'filament-cost-usd': 0.1,
            'print-time': datetime.timedelta(minutes=56, seconds=55)
        }]
        actual_result = mpp.scrape_time_and_usage_estimates(
            ['test/gcodes/support-test-0.1mm.gcode'])
        self.assertEqual(expected_result, actual_result)

    def test_scrape_time_and_usage_estimates_from_large_model_gcode(self):
        """
        sees if scrape_time function can get the data from a gcode
        """
        expected_result = [{
            'name-of-file': 'test/gcodes/large-box-0.3mm.gcode',
            'filament-used-m': 1151.44,
            'filament-used-cm3': 2769.5,
            'filament-used-g': 3434.2,
            'filament-cost-usd': 61.8,
            'print-time': datetime.timedelta(days=4, hours=3, minutes=14, 
                seconds=19)

        }]
        actual_result = mpp.scrape_time_and_usage_estimates(
            ['test/gcodes/large-box-0.3mm.gcode'])
        self.assertEqual(expected_result, actual_result)
