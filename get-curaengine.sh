#!/bin/bash

LATEST_APPIMAGE_URL='https://github.com/Ultimaker/Cura/releases/download/4.0.0/Cura-4.0.0.AppImage'
APPIMAGE_NAME='Cura'

if [ ! -d "bin" ]; then
  mkdir bin
fi
cd bin

wget -O $APPIMAGE_NAME.AppImage $LATEST_APPIMAGE_URL

echo "Super user permissions required to mount appimage as filesystem..."
sudo mkdir /mnt/CuraAppImage
sudo mount -o loop $APPIMAGE_NAME.AppImage /mnt/CuraAppImage

echo "copying CuraEngine to ./bin/"
cp /mnt/CuraAppImage/usr/bin/CuraEngine ./

cd ..
