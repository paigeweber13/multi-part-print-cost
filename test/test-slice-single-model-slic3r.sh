#!/bin/bash

SETTINGS_100_MICRON='--first-layer-height 0.15 --layer-height 0.1'
SETTINGS_200_MICRON='--first-layer-height 0.25 --layer-height 0.2'
SETTINGS_300_MICRON='--first-layer-height 0.35 --layer-height 0.3'
SETTINGS_350_MICRON='--first-layer-height 0.40 --layer-height 0.35'

MODEL_TO_SLICE='bulbasaur'

if [ ! -d "gcodes" ]; then
  mkdir getkeycodes
fi

# Usage: slic3r [ ACTIONS ] [ TRANSFORM ] [ OPTIONS ] [ file.stl ... ]
COMMAND="../bin/slic3r-pe.AppImage --slice --load profiles/slic3r-pe-config.ini $SETTINGS_200_MICRON models/$MODEL_TO_SLICE.stl --output gcodes/$MODEL_TO_SLICE-0.2mm.gcode"

echo "Command to run: $COMMAND"
$COMMAND
