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
        cls.expected_scrape_results_200micron = [
            {
                'name-of-file': 'test/gcodes/1cm-cube-0.2mm.gcode',
                'filament-used-m': 1.57,
                'filament-used-cm3': 3.8,
                'filament-used-g': 4.7,
                'filament-cost-usd': 0.1,
                'print-time': datetime.timedelta(minutes=18, seconds=47)
            },
            {
                'name-of-file': 'test/gcodes/2cm-cube-0.2mm.gcode',
                'filament-used-m': 9.34,
                'filament-used-cm3': 22.5,
                'filament-used-g': 27.9,
                'filament-cost-usd': 0.5,
                'print-time': datetime.timedelta(hours=1, minutes=34,
                                                 seconds=53)
            },
            {
                'name-of-file': 'test/gcodes/3cm-cube-0.2mm.gcode',
                'filament-used-m': 27.23,
                'filament-used-cm3': 65.5,
                'filament-used-g': 81.2,
                'filament-cost-usd': 1.5,
                'print-time': datetime.timedelta(hours=4, minutes=11,
                                                 seconds=53)
            }]

        cls.expected_aggregate_results_200micron = {
            'name-of-file': 'total',
            'filament-used-m': 38.14,
            'filament-used-cm3': 91.8,
            'filament-used-g': 113.8,
            'filament-cost-usd': 2.1,
            'print-time': datetime.timedelta(hours=6, minutes=5, seconds=33)
        }

        cls.print_bed_width = 220 # mm
        cls.print_bed_height = 220 # mm
        mpp.get_slic3r_pe()

    def test_slice_single_model(self):
        """
        tries to slice a single model with 0.2mm layer height and checks to see
        if the file exists. Not a really robust check, but it works
        """
        try:
            os.remove('test/models/gcodes/bulbasaur-0.2mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [[
            # 'bin/slic3r-pe.AppImage',
            mpp.BINARY,
            '--slice', '--load',
            'profiles/default-profile.ini', '--first-layer-height', '0.25',
            '--layer-height', '0.2',
            '--center', str(int(TestCoreFunctions.print_bed_width/2)) + ',' + \
            str(int(TestCoreFunctions.print_bed_height/2)),
            'test/models/bulbasaur.stl',
            '--output', 'test/models/gcodes/bulbasaur-0.2mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_models(0.2, False, \
                                         ['test/' + 'models/bulbasaur.stl']))
        self.assertTrue(os.path.isfile(
            'test/models/gcodes/bulbasaur-0.2mm.gcode'))

        try:
            os.remove('test/models/gcodes/bulbasaur-0.2mm.gcode')
        except FileNotFoundError:
            pass

    def test_slice_single_model_with_supports(self):
        """
        slices with supports and checks the generated time/usage estimates,
        which will be greater because of the support material
        """
        try:
            os.remove('test/models/gcodes/support-test-0.1mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [[
            # 'bin/slic3r-pe.AppImage',
            mpp.BINARY,
            '--slice', '--load',
            'profiles/default-profile.ini', '--first-layer-height', '0.15',
            '--layer-height', '0.1', '--support-material',
            '--center', str(int(TestCoreFunctions.print_bed_width/2)) + ',' + \
            str(int(TestCoreFunctions.print_bed_height/2)),
            'test/models/support-test.stl',
            '--output', 'test/models/gcodes/support-test-0.1mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_models(0.1, True,
                                         ['test/' +
                                          'models/support-test.stl']))
        self.assertTrue(os.path.isfile(
            'test/models/gcodes/support-test-0.1mm.gcode'))

        try:
            os.remove('test/models/gcodes/support-test-0.1mm.gcode')
        except FileNotFoundError:
            pass

    def test_slice_three_models_simultaneously(self):
        """
        slices multiple models to ensure behavior is still the same as when
        slicing one
        """
        try:
            os.remove('test/models/gcodes/1cm-cube-0.2mm.gcode')
            os.remove('test/models/gcodes/2cm-cube-0.2mm.gcode')
            os.remove('test/models/gcodes/3cm-cube-0.2mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [
            [
                # 'bin/slic3r-pe.AppImage',
                mpp.BINARY,
                '--slice', '--load',
                'profiles/default-profile.ini', '--first-layer-height',
                '0.25', '--layer-height', '0.2',
                '--center', str(int(TestCoreFunctions.print_bed_width/2)) \
                + ',' + str(int(TestCoreFunctions.print_bed_height/2)),
                'test/models/1cm-cube.stl',
                '--output', 'test/models/gcodes/1cm-cube-0.2mm.gcode'
            ],
            [
                # 'bin/slic3r-pe.AppImage',
                mpp.BINARY,
                '--slice', '--load',
                'profiles/default-profile.ini', '--first-layer-height',
                '0.25', '--layer-height', '0.2',
                '--center', str(int(TestCoreFunctions.print_bed_width/2)) + \
                ',' + str(int(TestCoreFunctions.print_bed_height/2)),
                'test/models/2cm-cube.stl',
                '--output', 'test/models/gcodes/2cm-cube-0.2mm.gcode'
            ],
            [
                # 'bin/slic3r-pe.AppImage',
                mpp.BINARY,
                '--slice', '--load',
                'profiles/default-profile.ini', '--first-layer-height',
                '0.25', '--layer-height', '0.2',
                '--center', str(int(TestCoreFunctions.print_bed_width/2)) \
                + ',' + str(int(TestCoreFunctions.print_bed_height/2)),
                'test/models/3cm-cube.stl',
                '--output', 'test/models/gcodes/3cm-cube-0.2mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_models(0.2, False,
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
        expected.insert(0, \
            TestCoreFunctions.expected_aggregate_results_200micron)
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

    def test_slice_model_that_isnt_centered(self):
        """
        models that were not centered would fail with an unhelpful message.
        This test ensures that non-centered models get fixed first
        """
        try:
            os.remove('test/models/gcodes/crank-0.3mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [
            [
                # 'bin/slic3r-pe.AppImage',
                mpp.BINARY,
                '--slice', '--load',
                'profiles/default-profile.ini', '--first-layer-height',
                '0.35', '--layer-height', '0.3', '--center',
                str(int(TestCoreFunctions.print_bed_width/2)) + ',' + \
                str(int(TestCoreFunctions.print_bed_height/2)),
                'test/models/crank.stl', '--output',
                'test/models/gcodes/crank-0.3mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_models(0.3, False,
                                         ['test/' + 'models/crank.stl']))
        self.assertTrue(os.path.isfile(
            'test/models/gcodes/crank-0.3mm.gcode'))

        try:
            os.remove('test/models/gcodes/crank-0.3mm.gcode')
        except FileNotFoundError:
            pass
    
    def test_slice_model_with_custom_profile(self):
        """
        """
        try:
            os.remove('test/models/gcodes/1cm-cube-0.2mm.gcode')
        except FileNotFoundError:
            pass

        expected_commands = [
            [
                mpp.BINARY,
                '--slice', '--load',
                'profiles/airplane-ender3.ini', '--first-layer-height',
                '0.25', '--layer-height', '0.2', '--center',
                str(int(TestCoreFunctions.print_bed_width/2)) + ',' + \
                str(int(TestCoreFunctions.print_bed_height/2)),
                'test/models/1cm-cube.stl', '--output',
                'test/models/gcodes/1cm-cube-0.2mm.gcode'
            ]]
        self.assertEqual(expected_commands,
                         mpp.slice_models(0.2, False,
                                         ['test/' + 'models/1cm-cube.stl'],
                                         profile='profiles/airplane-ender3.ini'))
        self.assertTrue(os.path.isfile(
            'test/models/gcodes/1cm-cube-0.2mm.gcode'))

        try:
            os.remove('test/models/gcodes/1cm-cube-0.2mm.gcode')
        except FileNotFoundError:
            pass
