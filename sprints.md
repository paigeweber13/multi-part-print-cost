# Sprint
## Target Release Date: 2019-05-26
## Goals:
 - [x] have basic GUI that takes input .stl files and outputs a prediction in a
   text file.
 - [x] make output properly formatted
 - [ ] make it work cross-platform
 - [ ] DEPLOY BINARIES
   - how do I want to deploy? How hard is it to make an appimage? how hard is
     it to deploy to PyPi? I think I'm going to start by building .exe files
     for windows and mac/linux users can just run from source
### Stretch:
 - [ ] fix loading gif
 - [ ] update readme
 - [ ] deploy to pypi

# Icebox
 - [ ] do I want to remove clamp-bolt? We don't use it. Could I use it at some
   point?
 - [ ] travis-ci for AppImage building, windows exe creation, etc.
 - [ ] modify text output: just show file name, not full path. still clip off
   long names.
 - [ ] in file where print stats are output, include print settings and
   location of gcodes
 - [ ] file names: don't include layer height
 - [ ] create GUI
 - [ ] make it work with arbitrary exported slic3r profile
   - [ ] This will be useful when slicing airplane parts!
 - [ ] make it work with new PrusaSlicer

# Log of what's been done:
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
 - [x] make output sortable (by print time or filament usage... they should
       result in the same sorted order though right?)
 - [x] test length of text in name of gcode... maybe do full length in text
       file and short length in terminal? Mmm... it'd be useful to also have
       full length in terminal I think.
 - [x] run pylint, make requested changes
 - [x] ~~get newest version, even when newest version number changes~~
   - [x] ~~is this a good idea? what if they change how the gcode is
     formatted?~~
   - [x] this is a bad idea