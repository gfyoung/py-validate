#!/bin/bash

echo "Linting repository..."
source activate validate

flake8
