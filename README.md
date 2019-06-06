# Multi Part Print Cost
Calculates cumulative filament used and time taken for prints that have too many
parts to fit on one build plate. Uses Slic3r Prusa Edition on the backend, which
is released under the [AGPLv3
license](https://github.com/prusa3d/PrusaSlicer/blob/7308017ee82abc725e5eb7aff26839d3e963b566/LICENSE).
Source code for slic3r is available
[here](https://github.com/prusa3d/PrusaSlicer). No modifications to the slic3r
source code were made before redistributing.

## Justification
There are many interesting things that can be 3d-printed but require more parts
than can fit on a single build plate. One example is [ericthepoolboy's scale
model of a Toyota 4-cylinder engine](https://www.thingiverse.com/thing:644933).
It can be very useful to have a good estimate of how much this project would
cost (in both time and money) before beginning it. Enter this program.

# Getting Started
The easiest way to run multi-part-print-cost is to download a
[release](https://github.com/rileyweber13/muli-part-print-cost/releases),
extract it, and run. For now, this only works on windows. Other options are
listed below
## Run from source
 1. ensure that python 3 is installed
 1. install dependencies: `pip install --user PySimpleGUI`
 1. download or clone this repository: `git clone
    https://github.com/rileyweber13/muli-part-print-cost.git`
 1. enter the directory where the project resides: 
    `cd multi-part-print-cost`
 1. add the project directory to PYTHONPATH environment variable
    1. on mac/linux/other unix this can be done by executing `$PYTHONPATH=/path/ to/multi-part-print-cost:$PYTHONPATH`
       before running the following command
 1. in the root where the code is extracted, run `python3
    multipartprintpy/gui.py`
## Install and run using pip
Currently, I don't plan on targeting PyPi for builds. If you would like to
install multi-part-print-cost with pip, please show your interest by opening an
issue.

# Dependencies
 * python 3 (tested on versions 3.6.2 and above)
 * PySimpleGUI

# Print settings
Full information about the profile used is in `profiles/default-profile.ini`
The important details are summarized below:

all three use 3 perimeter, top, and bottom layers, and 20% cubic infill.
Printer-specific settings are based on Ender3, the printer I have on hand. But
time/cost estimates should be the same across single-extruder printers that use
the same filament.

Filament is assumed to be 1.75mm PLA. Density is assumed to be 1.24 g/cm3 and
cost is assumed to be $18 USD per KG. This is the cost of most of 3D Solutech's
rolls, which is my trusted brand.

# Compatibility:
Releases are currently only built for Windows 10 x64. Linux builds coming soon!
You can run from source on any platform that has a Python3 interpreter.
## Mac:
I don't have access to a mac. If you have one and would like to contribute by
testing code and building releases, please contact me at
rileyw13@protonmail.com. You can also just donate an old mac to me ;)
