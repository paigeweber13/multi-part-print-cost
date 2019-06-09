#!/bin/bash
cd ..
export PYTHONPATH=$PYTHONPATH:$(pwd)
pyinstaller build-files/multi-part-print-cost-unix.spec
chmod +x dist/multi-part-print-cost
cp README.md dist/
cp LICENSE dist/
cp -r bin dist/
cp -r profiles dist/

filename="version"
read VERSION < $filename
rm -r "multi-part-print-cost-$VERSION-unix"
mv "dist" "multi-part-print-cost-$VERSION-unix"
tar -czf multi-part-print-cost-$VERSION-unix.tgz multi-part-print-cost-$VERSION-unix
