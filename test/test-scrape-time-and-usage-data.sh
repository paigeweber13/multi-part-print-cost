#!/bin/bash

FILE_TO_LOAD='gcodes/bulbasaur*.gcode'

FILAMENT_USED_LINE=$(grep 'filament used' $FILE_TO_LOAD)
PRINT_TIME_LINE=$(grep 'estimated printing time' $FILE_TO_LOAD)

FILAMENT_USED_MM=$(echo $FILAMENT_USED_LINE | grep -o -E '[0-9]+\.[0-9]+mm' \
  | grep -o -E '[0-9]+\.[0-9]')
FILAMENT_USED_CM3=$(echo $FILAMENT_USED_LINE | grep -o -E '[0-9]+\.[0-9]+cm3' \
  | grep -o -E '[0-9]+\.[0-9]')
PRINT_TIME=$(echo $PRINT_TIME_LINE \
  | grep -o -E '([0-9]+h)? ([0-9]+m)? ([0-9]+s)?')

echo "Filament used: $FILAMENT_USED_MM mm"
echo "Filament used: $FILAMENT_USED_CM3 cm3"
echo "Print time:    $PRINT_TIME"
