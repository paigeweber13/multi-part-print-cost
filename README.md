# Multi Part Print Cost
Calculates cumulative filament used and time taken for prints that have
multiple parts. Uses Slic3r Prusa Edition on the backend.

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

## TODO:
 - [x] how will I add times together? Make time object? Switch language?
   - [x] Is there any benefit in continuing to use bash over something like
         python?
   - [x] Can I run slic3r appimage from python?
 - [x] how to get gcode to actually include filament cost?
 - [x] get approx filament cost from slic3r gcode
 - [x] test scrape from support-test.gcode
 - [x] what happens if the model takes more than a day?
 - [x] test scrape from large-box.gcode
 - [x] clean up code
 - [x] write tests for slicing/scraping multiple models
 - [x] write function that aggregates results of scraping data from gcodes
 - [x] port get-slic3r-pe.sh to a python function in core.py
 - [x] combine it all, build an interface
 - [x] make tests faster
   - [x] look at pytest-profiling (ended up using pytest --durations=0)
   - [x] how can I make a fast test that will give a multiple-day print time?
     - [x] don't need to slice the model! Just need to scrape data from gcode.
       The function that has the edge case with multi-day prints is the scrape
       function.
 - [x] fix error when slicing crank.stl that says there are no layers
   - [x] start by writing a failing test for crank.
 - [x] add argparse so I can add things like output
 - [x] make it so I can save output to file
 - [ ] make output sortable (by print time or filament usage... they should
       result in the same sorted order though right?)
 - [ ] test length of text in name of gcode... maybe do full length in text
       file and short length in terminal? Mmm... it'd be useful to also have
       full length in terminal I think.
 - [ ] run pylint, make requested changes
 - [ ] do I want to remove clamp-bolt? We don't use it. Could I use it at some
   point?
 - [ ] create GUI
 - [ ] get newest version, even when newest version number changes
   - [ ] is this a good idea? what if they change how the gcode is formatted?
 - [ ] make it work with arbitrary exported slic3r profile
 - [ ] make it work with new PrusaSlicer

## Compatibility:
only works with mac/linux/other unix-based operating systems. If there is
enough interest, I will work on a windows port.
