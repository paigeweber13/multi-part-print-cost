#!/bin/bash

LATEST_APPIMAGE_URL='https://github.com/prusa3d/Slic3r/releases/download/version_1.42.0-beta2/Slic3rPE-1.42.0-beta2+linux64-full-201904140843.AppImage'
APPIMAGE_NAME='slic3r-pe'

if [ ! -d "bin" ]; then
  mkdir bin
fi
cd bin

wget -O $APPIMAGE_NAME.AppImage $LATEST_APPIMAGE_URL
