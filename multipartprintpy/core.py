"""
a collection of tools to slice .stl files and get filament usage and
time-to-print estimates from .gcode files.

assumes this module is being run from the root of the package directory.
"""

import argparse
import datetime
import operator
import os
import re
import requests
import subprocess
import sys
import typing
import zipfile

CONFIG_FILE = 'profiles/default-profile.ini'
DOWNLOAD_DIR = 'bin'
BINARY = DOWNLOAD_DIR + '/slic3r-pe'
DOWNLOAD_LOCATION = None
DOWNLOAD_URL = None
OS = None

def get_slic3r_pe():
    set_os_specific_variables()
    
    if not os.path.isdir(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
    
    if not os.path.isfile(BINARY):
        # download if it's not there
        if not os.path.isfile(DOWNLOAD_LOCATION):
            response = requests.get(DOWNLOAD_URL)
            with open(DOWNLOAD_LOCATION, 'wb') as downloaded_file:
                downloaded_file.write(response.content)

        # on windows, unzip
        if OS == 'win32':
            zip_ref = zipfile.ZipFile(DOWNLOAD_LOCATION, 'r')
            zip_ref.extractall(DOWNLOAD_DIR)
            zip_ref.close()
            os.remove(DOWNLOAD_LOCATION)

        # try to change permissions
        try:
            subprocess.run(['chmod', '+x', BINARY])
        except FileNotFoundError:
            # if chmod isn't installed (e.g. on windows) do nothing
            pass

def set_os_specific_variables():
    global DOWNLOAD_URL
    global BINARY
    global DOWNLOAD_LOCATION
    global OS
    # these two lines enforces that this function runs at most once during the
    # lifetime of this process
    if DOWNLOAD_URL is not None:
        return

    linux_binary_url = 'https://github.com/prusa3d/Slic3r/releases/download/version_1.42.0-beta2/Slic3rPE-1.42.0-beta2+linux64-full-201904140843.AppImage'
    mac_binary_url = 'https://github.com/prusa3d/PrusaSlicer/releases/download/version_1.42.0-beta2/Slic3rPE-1.42.0-beta2+full-201904140836.dmg'
    win64_binary_url = 'https://github.com/prusa3d/PrusaSlicer/releases/download/version_1.42.0-beta2/Slic3rPE-1.42.0-beta2+win64-full-201904140830.zip'
    win32_binary_url = 'https://github.com/prusa3d/PrusaSlicer/releases/download/version_1.42.0-beta2/Slic3rPE-1.42.0-beta2+win32-full-201904140831.zip'
    
    OS = sys.platform.lower()
    # is 'windows' the right label? Test this.
    if OS == 'win32':
        # just always download win64 binary because it's far more common
        DOWNLOAD_URL = win64_binary_url
        DOWNLOAD_LOCATION = BINARY
        DOWNLOAD_LOCATION += '.zip'
        BINARY = DOWNLOAD_DIR + \
            '/Slic3rPE-1.42.0-beta2+win64-full-201904140830/slic3r.exe'
    elif OS == 'linux':
        DOWNLOAD_URL = linux_binary_url
        BINARY += '.AppImage'
        DOWNLOAD_LOCATION = BINARY
    elif OS == 'mac':
        # 'mac' is probably not the right name? maybe Darwin? I need a mac to 
        # test it...
        DOWNLOAD_URL = mac_binary_url
        BINARY += '.dmg'
        DOWNLOAD_LOCATION = BINARY
    else:
        print('could not detect operating system!')
        sys.exit(-1)

def get_gcode_output_path(model_path: str, layer_height: float):
    """
    returns a string representing the path where the gcodes should be output.
    Also ensures that intermediate directories are created.
    """
    split_path = model_path.split('/')
    gcode_directory = '/'.join(split_path[:-1]) + '/gcodes/'
    # print("gcode_directory:", gcode_directory)
    if not os.path.isdir(gcode_directory):
        os.makedirs(gcode_directory)

    output_file_path = gcode_directory + split_path[-1][:-4] + '-' + \
        str(layer_height) + 'mm.gcode'
    return output_file_path

def slice_models(layer_height: float, supports: bool,
                path_to_models: typing.List[str]):
    """
    slices model using slic3r-pe
    """
    if not isinstance(path_to_models, list):
        print("ERROR: input to slice_models must be a list!")
        return []

    get_slic3r_pe()
    print_bed_width = 220 # mm
    print_bed_height = 220 # mm
    list_of_commands = []
    layer_height = round(layer_height, 2)
    first_layer_height = round(layer_height+0.05, 2)

    for model in path_to_models:
        print("INFO: slicing", model)
        output_file_path = get_gcode_output_path(model, layer_height)
        command = [BINARY, '--slice', '--load',
                   CONFIG_FILE, '--first-layer-height', 
                   str(first_layer_height), '--layer-height',
                   str(layer_height), 
                   '--center', str(int(print_bed_width/2)) + ',' + \
                   str(int(print_bed_height/2)),
                   model, '--output',
                   output_file_path]
        if supports:
           command.insert(8, '--support-material')
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
        print("INFO: scraping data from", gcode_file)
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
            continue

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
    slice_models(layer_height, supports, models)
    gcode_names = []
    for model in models:
        gcode_names.append(get_gcode_output_path(model, layer_height))
    
    stats = scrape_time_and_usage_estimates(gcode_names)
    stats.insert(0, aggregate_data(stats))

    return stats

def output_results(results, output_file:str=None):
    """
    also returns string object of output
    """
    output_string = ''
    header = '{:>60s} | {:>7s} | {:>6s} | {:>6s} | {:>5s} | {:17s}'.format(
        'Name of File', 'm', 'cm3', 'g', '$', 'dd:hh:mm')
    output = None

    if output_file is not None:
        try:
            output = open(output_file, 'w')
            output.write(header + '\n')
        except IOError:
            print("can't open output file! Are you trying to access a folder" \
                + " that doesn't exist?\nContinuing without writing to file\n")

    print(header)
    output_string += header + '\n'
    results.sort(key=operator.itemgetter('filament-used-g'), reverse=True)

    for result in results:
        file_name = result['name-of-file']
        if len(result['name-of-file']) > 60:
            file_name = result['name-of-file'][-56:]
            file_name = '... ' + file_name
        row = '{:>60s} | {:7.2f} | {:6.1f} | {:6.1f} | {:5.2f} | {:17s}' \
            .format(file_name , result['filament-used-m'],
            result['filament-used-cm3'], result['filament-used-g'],
            result['filament-cost-usd'], str(result['print-time']))
        if output is not None:
            output.write(row + '\n')
        print(row)
        output_string += row + '\n'

    return output_string

def main():
    parser = argparse.ArgumentParser(
        description="""Calculate individual and aggregate print time for 
        multiple .stl files""")
    parser.add_argument('files', metavar='model', type=str, nargs='+',
                    help="""models to predict print time and filament usage""")
    parser.add_argument('-l', '--layer-height', metavar='height-in-mm', 
                    type=float, nargs=1, required=True, dest='layer_height',
                    help="""height of each layer""")
    parser.add_argument('-s', '--supports', required=False, dest='supports',
                    action='store_true',
                    help="""include if you want supports to be generated""")
    parser.add_argument('-o', '--output-file', metavar='file-name', nargs=1, 
                    required=False, dest='output_file',
                    help="""include if you want data to be output to a file on 
                    disk""")
    args = None
    try:
        args = parser.parse_args()
    except (ValueError, TypeError):
        parser.print_help()
        sys.exit(1)

    files_to_slice = args.files
    layer_height = args.layer_height[0]
    generate_supports = args.supports
    output_file = None
    if args.output_file:
        output_file = args.output_file[0]
    results = None

    try:
        results = compute_stats(layer_height, generate_supports, 
            files_to_slice)
    except ValueError:
        parser.print_help()
        sys.exit(1)
    
    print('\nSlicing complete! Outputting statistics of filament usage in ' +\
        'various units.\n')
    output_results(results, output_file)

if __name__ == '__main__':
    main()
