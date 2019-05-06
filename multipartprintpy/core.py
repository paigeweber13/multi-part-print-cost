"""
assumes this module is being run from the root of the package directory
"""

import datetime
import re
import subprocess
import typing

CONFIG_FILE = 'profiles/slic3r-pe-config.ini'
BINARY_LOCATION = 'bin/slic3r-pe.AppImage'

def slice_model(layer_height: float, supports: bool, path_to_model: str):
    """
    slices model using slic3r. Must run get-slic3r-pe.sh first
    """
    command = [BINARY_LOCATION, '--slice', '--load',
               CONFIG_FILE, '--first-layer-height', str(layer_height+0.05),
               '--layer-height', str(layer_height), path_to_model, '--output',
               path_to_model[:-4] + '-' + str(layer_height) + 'mm.gcode']
    subprocess.run(command)
    return command

def scrape_time_and_usage_estimates(list_of_files: typing.List[str]):
    """
    gets estimates on time to print and filament usage from a slic3r gcode
    """
    result = []
    estimate_regex = re.compile(
        r"""
        ^;\ filament\ used\ =\ (?P<mm_usage>\d+\.\d+)mm
        \ \((?P<cm3_usage>\d+\.\d+)cm3\)\n
        ;\ filament\ used\ =\ (?P<g_usage>\d+\.\d+)\n
        ;\ filament\ cost\ =\ (?P<usd_cost>\d+\.\d+)\n
        .*\n
        ;\ estimated\ printing\ time\ \(normal\ mode\)\ =\ (?P<time>(\d+h
        \ )?(\d+m\ )?\d+s)$
        """, re.VERBOSE | re.MULTILINE)
    for gcode_file in list_of_files:
        my_match = None
        try:
            with open(gcode_file, 'r') as open_gcode:
                my_match = estimate_regex.search(open_gcode.read())
        except FileNotFoundError:
            print('file ' + gcode_file + ' not found, skipping...')
            continue
        
        print(my_match)

        filament_usage_m = round(float(my_match.group(
            'mm_usage')) / 1000, 2)
        print_time = datetime.datetime.strptime(my_match.group('time'),
            # '%Hh %Mm %Ss').time()
            '%Mm %Ss').time()
        result.append({
            'name-of-file': gcode_file,
            'filament-used-m': filament_usage_m,
            'filament-used-cm3': float(my_match.group('cm3_usage')),
            'filament-used-g': float(my_match.group('g_usage')),
            'filament-cost-usd': float(my_match.group('usd_cost')),
            'print-time': print_time,
        })
    return result
