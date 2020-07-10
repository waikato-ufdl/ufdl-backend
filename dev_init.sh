#!/bin/bash

function check_executable()
{
  if [ ! -x "/usr/bin/$EXEC" ]
  then
    echo	  
    echo "$EXEC executable not present!"
    echo "Install on Debian systems with:"
    echo "sudo apt-get install $EXEC $ADDITIONAL"
    echo	  
    exit 1
  fi
}

function check_repository()
{
  if [ ! -d "../$REPO" ]
  then
    echo	  
    echo "Directory ../$REPO does not exist!"
    echo "Check out repo as follows:"
    echo "cd .."
    echo "git clone https://github.com/waikato-ufdl/$REPO.git"
    echo	  
    exit 2
  fi
}

EXEC="virtualenv"
ADDITIONAL=""
check_executable
EXEC="python3.7"
ADDITIONAL="python3.7-dev"
check_executable

REPO="ufdl-json-messages"
check_repository

echo "Press any key to start setup of 'venv.dev' for running UFDL backend"
read -s -n 1 key

# delete old directory
if [ -d "./venv.dev" ]
then
  echo "Removing old virtual environment..."
  rm -rf ./venv.dev
fi

echo "Creating new virtual environment..."
virtualenv -p /usr/bin/python3.7 ./venv.dev

echo "Installing dependencies..."
./venv.dev/bin/pip install --upgrade pip
./venv.dev/bin/pip install --upgrade setuptools
./venv.dev/bin/pip install Cython
./venv.dev/bin/pip install numpy
# check for nvidia-smi and install GPU version
if [ -f "/usr/bin/nvidia-smi" ]
then
  ./venv.dev/bin/pip install tensorflow-gpu
else
  ./venv.dev/bin/pip install tensorflow
fi

echo "Installing UFDL modules..."
./venv.dev/bin/pip install ../ufdl-json-messages/
./venv.dev/bin/pip install ufdl-annotation-utils/
./venv.dev/bin/pip install ufdl-core-app/
./venv.dev/bin/pip install ufdl-image-classification-app/
./venv.dev/bin/pip install ufdl-object-detection-app/
./venv.dev/bin/pip install ufdl-speech-app/
./venv.dev/bin/pip install ufdl-api-site/

echo "Configuring backend (admin/admin user)..."
./venv.dev/bin/python -m ufdl.api_site.scripts.reset

echo "Start dev server with:"
echo "./venv.dev/bin/python -m ufdl.api_site.scripts.manage runserver"

echo "Server is running on:"
echo "localhost:8000"
