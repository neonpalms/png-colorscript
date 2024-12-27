#!/bin/bash

# Define constants
INSTALL_DIR='/usr/local/bin'
EXECUTABLE_NAME='png-colorscript'

# Ensure the script is executed with root privileges
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Use sudo."
    exit 1
fi

# Check if the executable exists in the installation directory
if [ -f "$INSTALL_DIR/$EXECUTABLE_NAME" ]; then
    # Remove the executable
    rm "$INSTALL_DIR/$EXECUTABLE_NAME"
    echo "$EXECUTABLE_NAME has been successfully removed from $INSTALL_DIR."
else
    echo "$EXECUTABLE_NAME not found in $INSTALL_DIR. Nothing to remove."
fi
