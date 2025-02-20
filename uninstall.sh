#!/bin/bash

INSTALL_DIR='/usr/local/bin'
EXECUTABLE_NAME='png-colorscript'

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Use sudo."
    exit 1
fi

# Check if the executable exists in the installation directory
if [ -f "$INSTALL_DIR/$EXECUTABLE_NAME" ]; then
    rm "$INSTALL_DIR/$EXECUTABLE_NAME" # Remove the executable
    echo "$EXECUTABLE_NAME has been successfully removed from $INSTALL_DIR."
else
    echo "$EXECUTABLE_NAME not found in $INSTALL_DIR. Nothing to remove."
fi
