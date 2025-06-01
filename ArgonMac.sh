#!/bin/bash

# URL of the Python file to download
PYTHON_FILE_URL="https://raw.githubusercontent.com/v-pun215/Argon/refs/heads/main/ArgonInstaller-mac.py"
PYTHON_FILE_NAME="ArgonInstaller-mac.py"

# Download the Python file
curl -L "$PYTHON_FILE_URL" -o "$PYTHON_FILE_NAME"

# Execute the downloaded Python file
python3 "$PYTHON_FILE_NAME"

# Delete the Python file after execution
rm -f "$PYTHON_FILE_NAME"