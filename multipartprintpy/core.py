import re
import subprocess
import typing

"""
assumes this module is being run from the root of the package directory
"""
CONFIG_FILE = 'profiles/slic3r-pe-config.ini'
BINARY_LOCATION = 'bin/slic3r-pe.AppImage'

def slice_model(layer_height: float, supports: bool, path_to_model: str):
    command = [BINARY_LOCATION, '--slice', '--load',
               CONFIG_FILE, '--first-layer-height', str(layer_height+0.05),
               '--layer-height', str(layer_height), path_to_model, '--output',
               path_to_model[:-4] + '-' + str(layer_height) + 'mm.gcode']
    subprocess.run(command)
    return command

def scrape_time_and_usage_estimates(list_of_files: typing.List[str]):
    result = []
    estimate_regex = re.compile(
        r"""
        ^;\ filament\ used\ =\ (?P<mm_usage>\d+\.\d+)mm
        \ \((?P<cm3_usage>\d+\.\d+)cm3\)\n
        ;\ filament\ used\ =\ (?P<g_usage>\d+\.\d+)\n
        ;\ filament\ cost\ =\ (?P<usd_cost>\d+\.\d+)\n
        .*\n
        ;\ estimated\ printing\ time\ \(normal\ mode\)\ =\ (?P<time>\d+h
        \ \d+m\ \d+s)$
        """, re.VERBOSE, re.MULTILINE)
    for gcode_file in list_of_files:
        try:
            with open(gcode_file, 'r') as f:
                estimate_match = estimate_regex.match(f.read())
                pass
        except FileNotFoundError:
            # not sure what to do here yet
            pass
    return result
