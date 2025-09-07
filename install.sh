#!/bin/bash

echo "Visual Studio Project Generator - Linux/Mac Setup"
echo "================================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed"
    echo "Please install Python 3 using your package manager:"
    echo "  Ubuntu/Debian: sudo apt update && sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed"
    echo "Installing pip3..."
    if command -v apt &> /dev/null; then
        sudo apt install python3-pip
    elif command -v dnf &> /dev/null; then
        sudo dnf install python3-pip
    elif command -v pacman &> /dev/null; then
        sudo pacman -S python-pip
    else
        echo "Please install pip3 manually for your system"
        exit 1
    fi
fi

echo "Installing dependencies..."
python3 -m pip install --user --upgrade pip
python3 -m pip install --user -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Setup completed successfully!"
    echo ""
    echo "How to run:"
    echo "  GUI Version: python3 GUIprojBuilder.py"
    echo "  CLI Version: python3 CLIprojBuilder.py"
    echo ""
    echo "If you get 'command not found', try:"
    echo "  python3 -m tkinter (to test GUI support)"
    echo "  If tkinter fails, install: sudo apt install python3-tk (Ubuntu/Debian)"
else
    echo "Failed to install dependencies"
    echo "Try running: python3 -m pip install --user customtkinter"
    exit 1
fi
