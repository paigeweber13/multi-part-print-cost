#!/bin/bash
INSTALL_DIRECTORY="lib"
LOG_DIR="./log/"
LOG_FILE="$LOG_DIR$(date -u +"%Y-%m-%dT%H:%M:%SZ").log"

if [ ! -d "$LOG_DIR" ]; then
  mkdir $LOG_DIR
fi

echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" > $LOG_FILE

PROTOBUF_SOURCE_URL='https://github.com/protocolbuffers/protobuf/archive/v3.7.1.tar.gz'
PROTOBUF_SOURCE_PATH='protobuf-3.7.1'

LIB_ARCUS_SOURCE_URL='https://github.com/Ultimaker/libArcus/archive/4.0.0.tar.gz'
LIB_ARCUS_SOURCE_PATH='libArcus-4.0.0'

CURAENGINE_SOURCE_URL='https://github.com/Ultimaker/CuraEngine/archive/4.0.0.tar.gz'
CURAENGINE_SOURCE_PATH='CuraEngine-4.0.0'

if [ -d "$INSTALL_DIRECTORY" ]; then
  if [ "$1" == 'clean' ]; then
    echo "cleaning" | tee -a $LOG_FILE
    rm -rf $INSTALL_DIRECTORY
  fi
else
  mkdir $INSTALL_DIRECTORY
fi
cd $INSTALL_DIRECTORY

# start with its dependencies
## 1. Protobuf
### 1.1 Libtool - protobuf dependency
if [ "$(grep -Ei 'debian|buntu|mint' /etc/*release)" ]; then
  # we are on a debian-based OS
  echo "Updating package repo..." | tee -a ../$LOG_FILE
  sudo apt-get update >> ../$LOG_FILE 2>&1
  sudo apt-get install libtool >> ../$LOG_FILE 2>&1
else
  echo "Make sure libtool is installed!"
fi

## continuing with protobuf
# only download and extract if those folders don't already exist
if [ ! -f "$PROTOBUF_SOURCE_PATH.tar.gz" ]; then
  echo "Downloading protobuf source..." | tee -a ../$LOG_FILE
  wget -O $PROTOBUF_SOURCE_PATH.tar.gz $PROTOBUF_SOURCE_URL
fi
if [ ! -d "$PROTOBUF_SOURCE_PATH" ]; then
  echo "Extracting protobuf..." | tee -a ../$LOG_FILE
  tar -xzf $PROTOBUF_SOURCE_PATH.tar.gz >> ../$LOG_FILE 2>&1
fi

# test if protoc is installed
echo "Testing protoc..." | tee -a ../$LOG_FILE
protoc --version 2>&1 | tee -a ../$LOG_FILE
if [ $? != 0 ]; then
  echo "Protoc is not installed, installing..." | tee -a ../$LOG_FILE
  # protoc is not installed!
  cd $PROTOBUF_SOURCE_PATH
  ./autogen.sh
  ./configure
  make
  sudo make install
  cd ..

  echo "Testing protoc again..." | tee -a ../$LOG_FILE
  protoc --version 2>&1 | tee -a ../$LOG_FILE
  if [ $? != 0 ]; then
    # something still went wrong...
    echo "Protoc could not be installed, check the log at $LOG_FILE" | tee -a ../$LOG_FILE
    exit 1
  fi
fi

## end protobuf

## 2. LibArcus
if [ ! -f "$LIB_ARCUS_SOURCE_PATH.tar.gz" ]; then
  wget -O $LIB_ARCUS_SOURCE_PATH.tar.gz $LIB_ARCUS_SOURCE_URL
fi
if [ ! -d "$LIB_ARCUS_SOURCE_PATH" ]; then
  tar -xzf $LIB_ARCUS_SOURCE_PATH.tar.gz
fi

### 2.1 cmake, python3-dev, and python3-sip-dev: Libarcus dependencies
if [ "$(grep -Ei 'debian|buntu|mint' /etc/*release)" ]; then
  # we are on a debian-based OS
  sudo apt-get install cmake
  sudo apt-get install python3-dev
  sudo apt-get install python3-sip-dev
else
  echo "Make sure cmake, python3-dev, and pythono3-sip-dev are installed!"
fi

# for now, always installs because I don't know how to check
cd $LIB_ARCUS_SOURCE_PATH
mkdir build 
cd build
cmake ..
make
sudo make install

cd ../..
# finally, CuraEngine itself
if [ ! -f "$CURAENGINE_SOURCE_PATH.tar.gz" ]; then
  wget -O $CURAENGINE_SOURCE_PATH.tar.gz $CURAENGINE_SOURCE_URL
fi
if [ ! -d "$CURAENGINE_SOURCE_PATH" ]; then
  tar -xzf $CURAENGINE_SOURCE_PATH.tar.gz 
fi
