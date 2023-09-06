#!/bin/bash

echo "Starting installation"

eval "$(conda shell.bash hook)"

ENV_NAME="koi-data-manager"
# conda create -n $ENV_NAME Python=3.11 -c conda-forge -y
conda create -n $ENV_NAME Python=3.11 -y
conda activate $ENV_NAME
echo "Env activated"

# codeartifact login
aws codeartifact login --tool pip --repository document --domain koireader --domain-owner 158511266486 --region us-west-2

# the below commented portion should not be uncommented unless mentioned
#echo "Installing poetry"
#curl -sSL https://install.python-poetry.org | python3 -
#echo "Poetry installed"
#poetry install --no-interaction
# echo "Poetry dependencies installed"


echo "installing dependencies"
pip install -r requirements.txt
echo "pip dependencies installed"
poetry install --only dev --no-interaction
echo "poetry development dependencies installed"

echo "Installing pre-commit and commit-msg hook"
pre-commit install
pre-commit install --hook-type commit-msg

echo "Setup done"
echo "Execute  'conda activate $ENV_NAME' "
