# Multi Part Print Cost
Calculates cumulative filament used and time taken for prints that have
multiple parts. Uses Slic3r Prusa Edition on the backend.

# Getting Started
There are a couple ways to run multi-part-print-cost.
## Run from source
 1. ensure that python 3 is installed
 1. install dependencies: `pip install --user PySimpleGUI`
 1. download or clone this repository: `git clone
    https://github.com/rileyweber13/muli-part-print-cost.git`
 1. enter the directory where the project resides: 
    `cd multi-part-print-cost`
 1. in the root where the code is extracted, run `python3
    multipartprintpy/gui.py`

# Dependencies
 * python 3 (tested on versions 3.6.2 and above)
 * PySimpleGUI

## Print settings
Full information about the profile used is in `profiles/slic3r-pe-config.ini`.
The important details are summarized below:

all three use 3 perimeter, top, and bottom layers, and 20% cubic infill.
Printer-specific settings are based on Ender3, the printer I have on hand. But
time/cost estimates should be the same across single-extruder printers that use
the same filament.

Filament is assumed to be 1.75mm PLA. Density is assumed to be 1.24 g/cm3 and
cost is assumed to be $18 USD per KG. This is the cost of most of 3D Solutech's
rolls, which is my trusted brand.

## Compatibility:
only works with linux and other operating systems capable of running the
slic3r-pe AppImage. I am currently working on windows compatibility.

# PROGRESS BAR TODO:
 - [ ] make slice_model error if it's not a list
 - [ ] make input to slice_model a list
 - [ ] make cancel button work
