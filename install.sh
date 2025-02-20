#!/bin/bash

INSTALL_DIR='/usr/local/bin'
EXECUTABLE_NAME='png-colorscript'

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Use sudo."
    exit 1
fi

# Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Build the standalone executable
pyinstaller --onefile "$EXECUTABLE_NAME.py"

# Exit the virtual environment
deactivate

# Move the executable to the installation directory
if [ -f "dist/$EXECUTABLE_NAME" ]; then
    mv "dist/$EXECUTABLE_NAME" "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/$EXECUTABLE_NAME" # Ensure it's executable
    echo "$EXECUTABLE_NAME has been installed to $INSTALL_DIR."
else
    echo "Build failed: Executable not found in dist/."
    exit 1
fi

# Clean up build files
rm -rf build dist "$EXECUTABLE_NAME.spec" .venv
