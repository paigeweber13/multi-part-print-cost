#!/bin/bash
cd ..
export PYTHONPATH=$PYTHONPATH:$(pwd)
pyinstaller build-files/multi-part-print-cost-unix.spec
chmod +x dist/multi-part-print-cost
cp README.md dist/
cp LICENSE dist/
cp -r bin dist/
cp -r profiles dist/