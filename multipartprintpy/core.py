"""
a collection of tools to slice .stl files and get filament usage and
time-to-print estimates from .gcode files.

assumes this module is being run from the root of the package directory.
"""

import datetime
import os
import re
import subprocess
import sys
import typing

CONFIG_FILE = 'profiles/slic3r-pe-config.ini'
BINARY_LOCATION = 'bin/slic3r-pe.AppImage'

def get_slic3r_pe():
    latest_appimage_url = 'https://github.com/prusa3d/Slic3r/releases/download/version_1.42.0-beta2/Slic3rPE-1.42.0-beta2+linux64-full-201904140843.AppImage'
    appimage_name = 'slic3r-pe.AppImage'
    download_dir = 'bin'
    
    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)
    
    subprocess.run(['wget', '-O', download_dir + '/' + appimage_name, 
        latest_appimage_url])
    subprocess.run(['chmod', '+x', download_dir + '/' + appimage_name])

def get_gcode_output_path(model_path: str, layer_height: float):
    """
    returns a string representing the path where the gcodes should be output.
    Also ensures that intermediate directories are created.
    """
    split_path = model_path.split('/')
    gcode_directory = '/'.join(split_path[:-1]) + '/gcodes/'
    if not os.path.isdir(gcode_directory):
        os.makedirs(gcode_directory)

    output_file_path = gcode_directory + split_path[-1][:-4] + '-' + \
        str(layer_height) + 'mm.gcode'
    return output_file_path

def slice_model(layer_height: float, supports: bool,
                path_to_models: typing.List[str]):
    """
    slices model using slic3r. Must run get-slic3r-pe.sh first
    """
    list_of_commands = []
    layer_height = round(layer_height, 2)
    first_layer_height = round(layer_height+0.05, 2)

    for model in path_to_models:
        output_file_path = get_gcode_output_path(model, layer_height)
        command = [BINARY_LOCATION, '--slice', '--load',
                   CONFIG_FILE, '--first-layer-height', 
                   str(first_layer_height), '--layer-height',
                   str(layer_height), model, '--output',
                   output_file_path]
        if supports:
           command.insert(9, '--support-material')
        list_of_commands.append(command)
        subprocess.run(command)
    return list_of_commands

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
        ;\ estimated\ printing\ time\ \(normal\ mode\)\ =
        \ (?P<time> (\d+d\ )? (\d+h\ )? (\d+m\ )? \d+s) $
        """, re.VERBOSE | re.MULTILINE)
    for gcode_file in list_of_files:
        my_match = None
        # print_time[0] is days, print_time[1] is hours, index 2 is minutes, 
        # and index 3 is seconds
        time_matches = []
        print_time = [0,0,0,0]

        try:
            with open(gcode_file, 'r') as open_gcode:
                my_match = estimate_regex.search(open_gcode.read())
                if my_match is None:
                    raise SyntaxError
                print_time_string = my_match.group('time')
                # print(print_time_string)
                time_matches.append(re.search(r'(\d+)d', print_time_string))
                time_matches.append(re.search(r'(\d+)h', print_time_string))
                time_matches.append(re.search(r'(\d+)m', print_time_string))
                time_matches.append(re.search(r'(\d+)s', print_time_string))
                # print(time_matches)
                for i in range(4):
                    if time_matches[i] is not None:
                        print_time[i] = int(time_matches[i].group(1))
        except FileNotFoundError:
            print('file ' + gcode_file + ' not found, skipping...')
            continue
        except SyntaxError:
            print('file ' + gcode_file + ' does not have properly formatted'
                + 'filament usage and time data. Skipping.')

        filament_usage_m = round(float(my_match.group(
            'mm_usage')) / 1000, 2)
        print_timedelta = datetime.timedelta(days=print_time[0],
            hours=print_time[1], minutes=print_time[2],
            seconds=print_time[3])

        result.append({
            'name-of-file': gcode_file,
            'filament-used-m': filament_usage_m,
            'filament-used-cm3': float(my_match.group('cm3_usage')),
            'filament-used-g': float(my_match.group('g_usage')),
            'filament-cost-usd': float(my_match.group('usd_cost')),
            'print-time': print_timedelta,
        })
    return result

def aggregate_data(print_estimates):
    """
    print_estimates is a dict with all the stats about a single sliced 
    model
    """
    aggregate = {
        'name-of-file': 'total',
        'filament-used-m': 0.0,
        'filament-used-cm3': 0.0,
        'filament-used-g': 0.0,
        'filament-cost-usd': 0.0,
        'print-time': datetime.timedelta(seconds=0),
    }
    for data in print_estimates:
        aggregate['filament-used-m'] += data['filament-used-m']
        aggregate['filament-used-cm3'] += data['filament-used-cm3']
        aggregate['filament-used-g'] += data['filament-used-g']
        aggregate['filament-cost-usd'] += data['filament-cost-usd']
        aggregate['print-time'] += data['print-time']

    aggregate['filament-used-m'] = round(aggregate['filament-used-m'], 2)
    aggregate['filament-used-cm3'] = round(aggregate['filament-used-cm3'], 2)
    aggregate['filament-used-g'] = round(aggregate['filament-used-g'], 2)
    aggregate['filament-cost-usd'] = round(aggregate['filament-cost-usd'], 2)

    return aggregate

def compute_stats(layer_height: float, supports: bool,
                  models: typing.List[str]):
    """
    wrapper function that takes paths to models and returns time and filament usage stats
    """
    slice_model(layer_height, supports, models)
    gcode_names = []
    for model in models:
        gcode_names.append(get_gcode_output_path(model, layer_height))
    
    stats = scrape_time_and_usage_estimates(gcode_names)
    stats.insert(0, aggregate_data(stats))

    return stats

def main():
    num_commands = len(sys.argv)
    if num_commands < 4:
        print('usage:', sys.argv[0],
            'layer-height supports? model[, model, ...]')
        return

    results = compute_stats(float(sys.argv[1]), bool(sys.argv[2]),
                            sys.argv[3:num_commands])
    
    print('Slicing complete! Outputting statistics of filament usage in ' +
        'various units.')
    print()
    print('%30s | %6s | %6s | %6s | %5s | %12s' % (
        'Name of File', 'm', 'cm3', 'g', '$', 'dd:hh:mm:ss'))
    for result in results:
        file_name = result['name-of-file']
        if len(result['name-of-file']) > 30:
            file_name = result['name-of-file'][-26:]
            file_name = '... ' + file_name
        print('%30s | %6.2f | %6.1f | %6.1f | %5.2f | %12s' % (
            file_name , result['filament-used-m'],
            result['filament-used-cm3'], result['filament-used-g'],
            result['filament-cost-usd'], result['print-time']))

if __name__ == '__main__':
    main()
