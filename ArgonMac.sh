#!/bin/bash

mkdir -p ArgonInstaller
# Change to the ArgonInstaller directory
cd ArgonInstaller || exit
# URL of the Python file to download
PYTHON_FILE_URL="https://raw.githubusercontent.com/v-pun215/Argon/refs/heads/main/ArgonInstaller-mac.py"
PYTHON_FILE_NAME="ArgonInstaller-mac.py"

# Download the Python file
curl -L "$PYTHON_FILE_URL" -o "$PYTHON_FILE_NAME"
python3 -m venv argonvenv
source argonvenv/bin/activate
# Execute the downloaded Python file
python3 "$PYTHON_FILE_NAME"
