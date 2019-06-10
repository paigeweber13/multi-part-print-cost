#!/bin/bash
cd ..
export PYTHONPATH=$PYTHONPATH:$(pwd)
rm -r dist
pyinstaller build-files/multi-part-print-cost-linux.spec
chmod +x dist/multi-part-print-cost
cp README.md dist/
cp LICENSE dist/
cp -r bin dist/
cp -r profiles dist/

version_filename="version"
read VERSION < $version_filename
output_filename="multi-part-print-cost-$VERSION-linux"
rm -r $output_filename
mv "dist" $output_filename
tar -czf $output_filename.tgz $output_filename
mkdir dist
mv $output_filename dist/
mv $output_filename.tgz dist/
