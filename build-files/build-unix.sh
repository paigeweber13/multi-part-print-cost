#!/bin/bash
cd ..
export PYTHONPATH=$PYTHONPATH:$(pwd)
pyinstaller build-files/multi-part-print-cost.spec
cp README.md dist/
cp LICENSE dist/
cp bin dist/
cp profiles dist/
