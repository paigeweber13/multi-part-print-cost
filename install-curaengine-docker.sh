#!/bin/bash

PROTOBUF_SOURCE_URL='https://github.com/protocolbuffers/protobuf/archive/v3.7.1.tar.gz'
PROTOBUF_SOURCE_PATH='protobuf-3.7.1'

LIB_ARCUS_SOURCE_URL='https://github.com/Ultimaker/libArcus/archive/4.0.0.tar.gz'
LIB_ARCUS_SOURCE_PATH='libArcus-4.0.0'

CURAENGINE_SOURCE_URL='https://github.com/Ultimaker/CuraEngine/archive/4.0.0.tar.gz'
CURAENGINE_SOURCE_PATH='CuraEngine-4.0.0'

mkdir lib
cd lib

## 1. protobuf
wget -O $PROTOBUF_SOURCE_PATH.tar.gz $PROTOBUF_SOURCE_URL
tar -xzf $PROTOBUF_SOURCE_PATH.tar.gz

cd $PROTOBUF_SOURCE_PATH
./autogen.sh
./configure
make
make install
cd ..
## end protobuf

## 2. LibArcus
wget -O $LIB_ARCUS_SOURCE_PATH.tar.gz $LIB_ARCUS_SOURCE_URL
tar -xzf $LIB_ARCUS_SOURCE_PATH.tar.gz

# libraries seem to be in /usr/local/lib
export CMAKE_INCLUDE_PATH=$CMAKE_INCLUDE_PATH:$(pwd)/protobuf-3.7.1/src
export CMAKE_LIBRARY_PATH=$CMAKE_LIBRARY_PATH:$(pwd)/protobuf-3.7.1/src/.libs

cd $LIB_ARCUS_SOURCE_PATH
mkdir build 
cd build
cmake ..
make
make install

cd ../..

## 3. finally, CuraEngine itself
wget -O $CURAENGINE_SOURCE_PATH.tar.gz $CURAENGINE_SOURCE_URL
tar -xzf $CURAENGINE_SOURCE_PATH.tar.gz 

cd $CURAENGINE_SOURCE_PATH
mkdir build
cd build
cmake ..
make
