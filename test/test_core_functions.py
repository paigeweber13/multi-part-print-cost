"""
tests core functionality. assumes that you are running tests from the root of
the project directory
"""

import copy
import datetime
import os
import unittest

import multipartprintpy.core as mpp

class TestCoreFunctions(unittest.TestCase):
    """
    tests things like slicing models and parsing the time/filament usage data
    """
    @classmethod
    def setUpClass(cls):
        cls.expected_scrape_results_200micron = [{
            'name-of-file': 'test/gcodes/1cm-cube-0.2mm.gcode',
            'filament-used-m': 0.86,
            'filament-used-cm3': 2.1,
            'filament-used-g': 2.6,
            'filament-cost-usd': 0.0,
            'print-time': datetime.timedelta(minutes=11, seconds=4)
        },
        {
            'name-of-file': 'test/gcodes/2cm-cube-0.2mm.gcode',
            'filament-used-m': 4.99,
            'filament-used-cm3': 12.0,
            'filament-used-g': 14.9,
            'filament-cost-usd': 0.3,
            'print-time': datetime.timedelta(minutes=54, seconds=51)
        },
        {
            'name-of-file': 'test/gcodes/3cm-cube-0.2mm.gcode',
            'filament-used-m': 14.36,
            'filament-used-cm3': 34.5,
            'filament-used-g': 42.8,
            'filament-cost-usd': 0.8,
            'print-time': datetime.timedelta(hours=2, minutes=23, seconds=20)
        }]

        cls.expected_aggregate_results_200micron = {
            'name-of-file': 'total',
            'filament-used-m': 20.21,
            'filament-used-cm3': 48.6,
            'filament-used-g': 60.3,
            'filament-cost-usd': 1.1,
            'print-time': datetime.timedelta(hours=3, minutes=29, seconds=15)
        }

    def test_slice_single_model(self):
        """
        tries to slice a single model with 0.2mm layer height and checks to see if the file exists. Not a really robust check, but it works
        """
        try:
            os.remove('test/models/gcodes/bulbasaur-0.2mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [[
            'bin/slic3r-pe.AppImage', '--slice', '--load',
            'profiles/slic3r-pe-config.ini', '--first-layer-height', '0.25',
            '--layer-height', '0.2', 'test/models/bulbasaur.stl',
            '--output', 'test/models/gcodes/bulbasaur-0.2mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_model(0.2, False, ['test/' +
                                         'models/bulbasaur.stl']))
        self.assertTrue(os.path.isfile(
            'test/models/gcodes/bulbasaur-0.2mm.gcode'))

        try:
            os.remove('test/models/gcodes/bulbasaur-0.2mm.gcode')
        except FileNotFoundError:
            pass

    def test_slice_single_model_with_supports(self):
        """
        """
        try:
            os.remove('test/models/gcodes/support-test-0.1mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [[
            'bin/slic3r-pe.AppImage', '--slice', '--load',
            'profiles/slic3r-pe-config.ini', '--first-layer-height', '0.15',
            '--layer-height', '0.1', 'test/models/support-test.stl', '--support-material', '--output',
            'test/models/gcodes/support-test-0.1mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_model(0.1, True, ['test/' +
                                         'models/support-test.stl']))
        self.assertTrue(os.path.isfile(
            'test/models/gcodes/support-test-0.1mm.gcode'))

        try:
            os.remove('test/models/gcodes/support-test-0.1mm.gcode')
        except FileNotFoundError:
            pass

    def test_slice_large_model(self):
        """
        """
        try:
            os.remove('test/models/gcodes/large-box-0.3mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [[
            'bin/slic3r-pe.AppImage', '--slice', '--load',
            'profiles/slic3r-pe-config.ini', '--first-layer-height', '0.35',
            '--layer-height', '0.3', 'test/models/large-box.stl', '--support-material', '--output',
            'test/models/gcodes/large-box-0.3mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_model(0.3, True, ['test/' +
                                         'models/large-box.stl']))
        self.assertTrue(os.path.isfile(
            'test/models/gcodes/large-box-0.3mm.gcode'))

        try:
            os.remove('test/models/gcodes/large-box-0.3mm.gcode')
        except FileNotFoundError:
            pass

    def test_slice_three_models_simultaneously(self):
        """
        """
        try:
            os.remove('test/models/gcodes/1cm-cube-0.2mm.gcode')
            os.remove('test/models/gcodes/2cm-cube-0.2mm.gcode')
            os.remove('test/models/gcodes/3cm-cube-0.2mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [[
            'bin/slic3r-pe.AppImage', '--slice', '--load',
            'profiles/slic3r-pe-config.ini', '--first-layer-height', '0.25',
            '--layer-height', '0.2', 'test/models/1cm-cube.stl', 
            '--output', 'test/models/gcodes/1cm-cube-0.2mm.gcode'
            ], [
            'bin/slic3r-pe.AppImage', '--slice', '--load',
            'profiles/slic3r-pe-config.ini', '--first-layer-height', '0.25',
            '--layer-height', '0.2', 'test/models/2cm-cube.stl', 
            '--output', 'test/models/gcodes/2cm-cube-0.2mm.gcode'
            ],
            [
            'bin/slic3r-pe.AppImage', '--slice', '--load',
            'profiles/slic3r-pe-config.ini', '--first-layer-height', '0.25',
            '--layer-height', '0.2', 'test/models/3cm-cube.stl', 
            '--output', 'test/models/gcodes/3cm-cube-0.2mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_model(0.2, False,
                                         [
                                         'test/models/1cm-cube.stl',
                                         'test/models/2cm-cube.stl',
                                         'test/models/3cm-cube.stl',
                                         ]))
        self.assertTrue(os.path.isfile(
            'test/models/gcodes/1cm-cube-0.2mm.gcode'))
        self.assertTrue(os.path.isfile(
            'test/models/gcodes/2cm-cube-0.2mm.gcode'))
        self.assertTrue(os.path.isfile(
            'test/models/gcodes/3cm-cube-0.2mm.gcode'))

        try:
            os.remove('test/models/gcodes/1cm-cube-0.2mm.gcode')
            os.remove('test/models/gcodes/2cm-cube-0.2mm.gcode')
            os.remove('test/models/gcodes/3cm-cube-0.2mm.gcode')
        except FileNotFoundError:
            pass

    def test_scrape_time_and_usage_estimates_from_gcode(self):
        """
        sees if scrape_time function can get the data from a gcode
        will fail if slic3r updates how it formats gcode comments
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

    def test_scrape_time_and_usage_estimates_from_three_gcode_files(self):
        """
        sees if scrape_time function can get the data from three gcodes 
        simultaneously
        """
        expected_result = TestCoreFunctions.expected_scrape_results_200micron
        actual_result = mpp.scrape_time_and_usage_estimates(
            ['test/gcodes/1cm-cube-0.2mm.gcode',
             'test/gcodes/2cm-cube-0.2mm.gcode',
             'test/gcodes/3cm-cube-0.2mm.gcode'])
        self.assertEqual(expected_result, actual_result)

    def test_aggregate_data(self):
        """
        just makes sure everything gets added together nicely when adding up
        total print time.
        """
        individual_results = \
            TestCoreFunctions.expected_scrape_results_200micron
        expected_result = \
            TestCoreFunctions.expected_aggregate_results_200micron
        
        self.assertEqual(expected_result,
            mpp.aggregate_data(individual_results))
        
    def test_compute_stats_wrapper_function(self):
        """
        will fail if slic3r updates the way it predicts time and filament usage
        """
        try:
            os.remove('test/models/gcodes/1cm-cube-0.2mm.gcode')
            os.remove('test/models/gcodes/2cm-cube-0.2mm.gcode')
            os.remove('test/models/gcodes/3cm-cube-0.2mm.gcode')
        except FileNotFoundError:
            pass

        actual = mpp.compute_stats(0.2, False, 
            [
                'test/models/1cm-cube.stl',
                'test/models/2cm-cube.stl',
                'test/models/3cm-cube.stl'
            ])
        expected = copy.deepcopy(\
            TestCoreFunctions.expected_scrape_results_200micron)
        print(expected)
        expected.insert(0, \
            TestCoreFunctions.expected_aggregate_results_200micron)
        print(TestCoreFunctions.expected_aggregate_results_200micron)
        expected[1]['name-of-file'] = \
            'test/models/gcodes/1cm-cube-0.2mm.gcode'
        expected[2]['name-of-file'] = \
            'test/models/gcodes/2cm-cube-0.2mm.gcode'
        expected[3]['name-of-file'] = \
            'test/models/gcodes/3cm-cube-0.2mm.gcode'
        self.assertEqual(expected, actual)

        try:
            os.remove('test/models/gcodes/1cm-cube-0.2mm.gcode')
            os.remove('test/models/gcodes/2cm-cube-0.2mm.gcode')
            os.remove('test/models/gcodes/3cm-cube-0.2mm.gcode')
        except FileNotFoundError:
            pass
