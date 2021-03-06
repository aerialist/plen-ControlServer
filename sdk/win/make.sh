#!/bin/bash

# author    : Kazuyuki TAKASE
# copyright : PLEN Project Company Inc, and all authors.
# license   : The MIT License


# Set environment variable & shell variable.
# =============================================================================
export APP_VERSION=`git tag | tail -n1`
APP_VERSION=${APP_VERSION:1}

cd ../../
REPOSITORY_ROOT=`pwd`


# Run the packaging script.
# =============================================================================
cd "${REPOSITORY_ROOT}/sdk/win/"
cp make.py "${REPOSITORY_ROOT}/control_server/"

cd "${REPOSITORY_ROOT}/control_server/"
python make.py py2exe


# Set up core components' files and directories.
# =============================================================================
cp config.json ./dist
cp device_map.json ./dist

cd ./dist
mv main.exe ControlServer.exe
mkdir logs
mkdir views
cat << __URL_FILE_EOL__ > PLEN_Utils.url
[InternetShortcut]
URL=http://localhost:17264/
__URL_FILE_EOL__
rm -rf tcl w9xpopen.exe


# Tear down unnecessary files and directories.
# =============================================================================
cd ..
rm -rf build make.py


# Set up GUI components' files and directories.
# =============================================================================
cd "${REPOSITORY_ROOT}/control_server_gui/control_server_gui/"
cp gui.html "${REPOSITORY_ROOT}/control_server/dist/views/"
cp -r angularjs "${REPOSITORY_ROOT}/control_server/dist/"
cp -r assets "${REPOSITORY_ROOT}/control_server/dist/"


# Rename the packaged application with version number.
# =============================================================================
cd "${REPOSITORY_ROOT}/control_server/"
mv dist ControlServer_Win_v${APP_VERSION}


# Show the prompt message.
# =============================================================================
echo -e "\nPlease enter any key to exit..."
read WAIT