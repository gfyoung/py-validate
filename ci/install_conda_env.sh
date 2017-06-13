#!/bin/bash

echo "Creating a Python $PYTHON_VERSION environment"
conda create -n validate python=$PYTHON_VERSION || exit 1
source activate validate

echo "Installing packages..."
conda install numpy flake8 pytest
