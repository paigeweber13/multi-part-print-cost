#!/bin/bash
INSTALL_DIRECTORY='lib'
PROTOBUF_BINARY_URL='https://github.com/protocolbuffers/protobuf/releases/download/v3.7.1/protoc-3.7.1-linux-x86_64.zip'
PROTOBUF_BINARY_PATH='protobuf-bin'

LIB_ARCUS_SOURCE_URL='https://github.com/Ultimaker/libArcus/archive/4.0.0.zip'
LIB_ARCUS_SOURCE_PATH='libarcus'

CURAENGINE_SOURCE_URL='https://github.com/Ultimaker/CuraEngine/archive/4.0.0.zip'
CURAENGINE_SOURCE_PATH='curaengine'

if [ -d "$INSTALL_DIRECTORY" ]; then
  rm -rf $INSTALL_DIRECTORY
fi
mkdir $INSTALL_DIRECTORY
cd $INSTALL_DIRECTORY

# start with its dependencies
## 1. Protobuf
### 1.1 Libtool
if [ "$(grep -Ei 'debian|buntu|mint' /etc/*release)" ]; then
  # we are on a debian-based OS
  sudo apt-get update
  sudo apt-get install libtool
  sudo apt-get install unzip
else
  echo "Make sure libtool and unzip are installed!"
fi

## continuing with protobuf
wget -O $PROTOBUF_BINARY_PATH.zip $PROTOBUF_BINARY_URL
unzip $PROTOBUF_BINARY_PATH.zip -d ./$PROTOBUF_BINARY_PATH
# add protoc to path
PATH=$(pwd)/$PROTOBUF_BINARY_PATH/bin:$PATH
# test protoc
#protoc --version
## end protobuf

## 2. LibArcus
wget -O $LIB_ARCUS_SOURCE_PATH.zip $LIB_ARCUS_BINARY_URL
unzip $LIB_ARCUS_BINARY_PATH.zip -d ./$LIB_ARCUS_BINARY_PATH
if [ "$(grep -Ei 'debian|buntu|mint' /etc/*release)" ]; then
  # we are on a debian-based OS
  sudo apt-get install cmake
  sudo apt-get install python3-dev
  sudo apt-get install python3-sip-dev
else
  echo "Make sure cmake, python3-dev, and pythono3-sip-dev are installed!"
fi

# finally, CuraEngine itself
wget -O $CURAENGINE_SOURCE_PATH.zip $CURAENGINE_BINARY_URL
unzip $CURAENGINE_BINARY_PATH.zip -d ./$CURAENGINE_BINARY_PATH
