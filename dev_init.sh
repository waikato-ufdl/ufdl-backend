#!/bin/bash

function check_executable()
{
  echo "Checking $EXEC..."
  if [ ! -x "/usr/bin/$EXEC" ]
  then
    AVAILABLE=false
    if [ "$REQUIRED" = "true" ]
    then
      echo
      echo "$EXEC executable not present!"
      echo "Install on Debian systems with:"
      echo "sudo apt-get install $EXEC $ADDITIONAL"
      echo
      exit 1
    else
      echo "...NOT present"
    fi
  else
    echo "...is present"
    AVAILABLE=true
  fi
}

function check_repository()
{
  echo "Checking repo $REPO..."
  if [ ! -d "../$REPO" ]
  then
    echo	  
    echo "Directory ../$REPO does not exist!"
    echo "Check out repo as follows:"
    echo "cd .."
    echo "git clone https://github.com/waikato-ufdl/$REPO.git"
    echo	  
    exit 2
  else
    echo "...is present"
  fi
}

echo "Performing checks"

EXEC="virtualenv"
ADDITIONAL=""
REQUIRED=true
check_executable

EXEC="python3.7"
ADDITIONAL="python3.7-dev"
REQUIRED=false
check_executable
PYTHON37_AVAILABLE=$AVAILABLE

EXEC="python3.8"
ADDITIONAL="python3.8-dev"
REQUIRED=false
check_executable
PYTHON38_AVAILABLE=$AVAILABLE

EXEC="mysql_config"
ADDITIONAL=""
REQUIRED=false
check_executable
MYSQLCONFIG_AVAILABLE=$AVAILABLE

if [ "MYSQLCONFIG_AVAILABLE" = "false" ]
then
  echo
  echo "mysql_config is not available, i.e., you won't be able to use MySQL as database backend."
  echo "Install on Debian systems with:"
  echo "  sudo apt-get install libmysqlclient-dev"
  echo
fi



if [ "$PYTHON37_AVAILABLE" = "false" ] && [ "$PYTHON38_AVAILABLE" = "false" ]
then
  echo
  echo "Neither Python 3.7 nor Python3.8 are available!"
  echo "Install on Debian systems with:"
  echo "  sudo apt-get install python3.7 python3.7-dev"
  echo "or"
  echo "  sudo apt-get install python3.8 python3.8-dev"
  echo
  exit 1
fi

if [ "$PYTHON37_AVAILABLE" = "true" ]
then
  PYTHON=python3.7
elif [ "$PYTHON38_AVAILABLE" = "true" ]
then
  PYTHON=python3.8
else
  echo "Don't know what Python executable to use!"
  exit 2
fi


REPO="ufdl-json-messages"
check_repository

if [ ! "$1" = "-y" ]
then
  echo
  echo "Press any key to start setup of 'venv.dev' for running UFDL backend (using $PYTHON)..."
  read -s -n 1 key
fi

# delete old directory
if [ -d "./venv.dev" ]
then
  echo "Removing old virtual environment..."
  rm -rf ./venv.dev
fi

echo "Creating new virtual environment..."
virtualenv -p /usr/bin/$PYTHON ./venv.dev

echo "Installing dependencies..."
./venv.dev/bin/pip install --upgrade pip
./venv.dev/bin/pip install --upgrade setuptools
./venv.dev/bin/pip install Cython
./venv.dev/bin/pip install numpy
if [ "$MYSQLCONFIG_AVAILABLE" = "true" ]
then
  ./venv.dev/bin/pip install mysqlclient
fi
./venv.dev/bin/pip install "opencv-python<4.2.0"
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
