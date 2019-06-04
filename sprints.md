# Sprint
## Target Release Date: 2019-06-02
## Goals:
 - [x] have basic GUI that takes input .stl files and outputs a prediction in a
   text file.
 - [x] make output properly formatted
 - [x] make it work cross-platform
   - [x] FIX FAILING TEST
     - okay so this is more complicated than it may 
     initially seem. The easiest way I can think of making this happen is by
     making the tests aware of the globals in core.... Which I don't even know
     if that's possible? Might be better to make core a class and make the
     globals into class variables.
     - potential solution: https://stackoverflow.com/a/3400652
 - [x] DEPLOY BINARIES
   - how do I want to deploy? How hard is it to make an appimage? 
     how hard is it to deploy to PyPi? I think I'm going to start by 
     building .exe files for windows and mac/linux users can just 
     run from source
   - [x] pyInstaller works
   - [x] test the exe
   - [x] fix loading gif
   - [x] make cancel button work
   - [x] find out why that one window is just hanging out when it's supposed to
     be closed?
   - [ ] 'slicing was cancelled' error always comes up, even when there is no
     error

I'm ready to release for this sprint, but it is too late to decide how to
package this thing tonight. I'll do that tomorrow. Code is done though!

### Stretch:
 - [ ] make build file for pyinstaller, add external files so that they get
   built into the .exe
 - [ ] set up continuous integration
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