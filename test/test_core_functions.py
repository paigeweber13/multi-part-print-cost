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
