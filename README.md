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
 [ ] make it work with arbitrary exported slic3r profile
