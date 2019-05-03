#!/bin/bash

SETTINGS_FOR_ALL='--fill-pattern cubic'

SETTINGS_100_MICRON='--first-layer-height 0.15 --layer-height 0.1'
SETTINGS_200_MICRON='--first-layer-height 0.25 --layer-height 0.2'
SETTINGS_300_MICRON='--first-layer-height 0.35 --layer-height 0.3'
SETTINGS_350_MICRON='--first-layer-height 0.40 --layer-height 0.35'

MODEL_TO_SLICE='models/bulbasaur.stl'

../bin/slic3r-pe.AppImage --slice $SETTINGS_FOR_ALL $SETTINGS_200_MICRON $MODEL_TO_SLICE
# to load settings from a file, use --load path/to/config.ini
