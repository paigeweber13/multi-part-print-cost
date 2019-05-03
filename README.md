# Multi Part Print Cost
Calculates cumulative filament used and time taken for prints that have
multiple parts. Uses Slic3r Prusa Edition on the backend.

## Print settings
Calculates by default with four different settings: 
0.1 mm layer height
0.2 mm layer height
0.3 mm layer height
0.35mm layer height
each case is calculated with and without supports.

all three use 3 perimeter, top, and bottom layers, and 20% cubic infill

## TODO:
 [ ] how will I add times together? Make time object? Switch language?
   [ ] Is there any benefit in continuing to use bash over something like
       python?
   [ ] Can I run slic3r appimage from python?
 [ ] get newest version, even when newest version number changes
 [ ] make it work with arbitrary exported slic3r profile

## Compatibility:
only works with mac/linux/other unix-based operating systems. If there is
enough interest, I will work on a windows port.
