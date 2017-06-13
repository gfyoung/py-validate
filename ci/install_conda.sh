#!/bin/bash

if [ -d "$HOME/miniconda3" ] && [ -e "$HOME/miniconda3/bin/conda" ]; then
    echo "Miniconda install already present from cache: $HOME/miniconda3"
    rm -rf $HOME/miniconda3/envs/stemming  # Just in case...
else
    echo "Installing Miniconda..."

    rm -rf $HOME/miniconda3  # Just in case...
    wget http://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh || exit 1
    bash miniconda.sh -b -p "$HOME/miniconda3" || exit 1
fi

echo "Configuring Miniconda..."
conda config --set ssl_verify false || exit 1
conda config --set always_yes true --set changeps1 false || exit 1

echo "Updating Miniconda"
conda update --all
conda info -a || exit 1
