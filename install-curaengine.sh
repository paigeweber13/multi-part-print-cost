#!/bin/bash
INSTALL_DIRECTORY='lib'
PROTOBUF_BINARY_URL='https://github.com/protocolbuffers/protobuf/releases/download/v3.7.1/protoc-3.7.1-linux-x86_64.zip'
PROTOBUF_BINARY_NAME='protobuf-bin'

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
wget -O $PROTOBUF_BINARY_NAME.zip $PROTOBUF_BINARY_URL
unzip $PROTOBUF_BINARY_NAME.zip -d ./$PROTOBUF_BINARY_NAME


    # Be sure to have libtool installed.
    # Download protobuf from https://github.com/google/protobuf/releases (download ZIP and unZIP at desired location, or clone the repo). The protocol buffer is used for communication between the CuraEngine and the GUI.
    # Run autogen.sh from the protobuf directory: $ ./autogen.sh
    # $ ./configure
    # $ make
    # # make install
    # (Please note the #. It indicates the need of superuser, as known as root, priviliges.)
    # (In case the shared library cannot be loaded, you can try sudo ldconfig on Linux systems)


git clone https://github.com/Ultimaker/libArcus.git

# finally, CuraEngine itself
git clone https://github.com/Ultimaker/CuraEngine.git
