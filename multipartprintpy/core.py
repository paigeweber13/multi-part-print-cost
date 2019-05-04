import subprocess

"""
assumes this module is being run from the root of the package directory
"""
CONFIG_FILE='profiles/slic3r-pe-config.ini'
BINARY_LOCATION='bin/slic3r-pe.AppImage'

def slice_model(layer_height: float, supports: bool, path_to_model: str):
    command = [BINARY_LOCATION, '--slice', '--load',
               CONFIG_FILE, '--first-layer-height', str(layer_height+0.05),
               '--layer-height', str(layer_height), path_to_model, '--output', 
               path_to_model[:-4] + '-' + str(layer_height) + 'mm.gcode']
    subprocess.run(command)
    return command