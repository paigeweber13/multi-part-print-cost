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
 [ ] how will I add times together? Make time object? Switch language?
   [ ] Is there any benefit in continuing to use bash over something like
       python?
   [ ] Can I run slic3r appimage from python?
 [x] how to get gcode to actually include filament cost?
 [ ] get approx filament cost from slic3r gcode
 [ ] get newest version, even when newest version number changes
 [ ] make it work with arbitrary exported slic3r profile

## Compatibility:
only works with mac/linux/other unix-based operating systems. If there is
enough interest, I will work on a windows port.
