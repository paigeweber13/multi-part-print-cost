#!/bin/bash

export CURA_ENGINE_SEARCH_PATH=/resources/definitions:/resources/extruders
SETTINGS_TO_USE=../bin/resources/definitions/fdmprinter.def.json
MODEL_TO_SLICE=bulbasaur.stl

../bin/CuraEngine slice -j $SETTINGS_TO_USE -l $MODEL_TO_SLICE
