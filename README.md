# Multi Part Print Cost
Calculates cumulative filament used and time taken for prints that have
multiple parts. Uses Slic3r Prusa Edition on the backend.

# Getting Started
There are a couple ways to run multi-part-print-cost.
## Run from source
 1. ensure that python 3 is installed
 1. download or clone this repository: `git clone
    https://github.com/rileyweber13/muli-part-print-cost.git`
 1. enter the directory where the project resides: `cd multi-part-print-cost`
 1. in the root where the code is extracted, run `python3
    multipartprintpy/gui.py`

# Dependencies
 * python 3 (tested on versions 3.6.2 and above)
 * PySimpleGUI

## Print settings
Full information about the profile used is in test/profiles. The important details are summarized below:

Calculates by default with four different settings: 
 * 0.1 mm layer height
 * 0.2 mm layer height
 * 0.3 mm layer height
 * 0.35mm layer height
each case is calculated with and without supports.

all three use 3 perimeter, top, and bottom layers, and 20% cubic infill.
Printer-specific settings based on Ender3, the printer I have on hand. But
time/cost estimates should be the same across single-extruder printers that use
the same filament.

Filament is assumed to be 1.75mm PLA. Density is assumed to be 1.24 g/cm3 and
cost is assumed to be $18 USD per KG. This is the cost of most of 3D Solutech's
rolls, which is my trusted brand.

## Compatibility:
only works with mac/linux/other unix-based operating systems. If there is
enough interest, I will work on a windows port.
