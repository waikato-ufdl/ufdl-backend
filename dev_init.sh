#!/bin/bash

#############
# FUNCTIONS #
#############

# the usage of this script
function usage()
{
   echo
   echo "${0##*/} [-y] [-u] [-h]"
   echo
   echo "Initializes the virtual environment for the UFDL backend."
   echo
   echo " -h   this help"
   echo " -y   do not prompt user, assume 'yes'"
   echo " -u   update any repositories first"
   echo " -r   skip database reset"
   echo
}

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
    exit 1
  else
    echo "...is present"
  fi
}

function update_repository()
{
  echo "Updating repo $REPO..."
  CURRENT="`pwd`"
  cd "../$REPO"
  git pull
  cd "$CURRENT"
}

##############
# PARAMETERS #
##############

VENV="venv.dev"
PROMPT="yes"
UPDATE="no"
RESET="yes"
while getopts ":hyur" flag
do
   case $flag in
      y) PROMPT="no"
         ;;
      u) UPDATE="yes"
         ;;
      h) usage
         exit 0
         ;;
      r) RESET="no"
         ;;
      *) usage
         exit 1
         ;;
   esac
done

##########
# CHECKS #
##########

echo "Performing checks"

EXEC="virtualenv"
ADDITIONAL=""
REQUIRED=true
check_executable

EXEC="python3.8"
ADDITIONAL="python3.8-dev"
REQUIRED=false
check_executable
PYTHON38_AVAILABLE=$AVAILABLE

EXEC="python3.10"
ADDITIONAL="python3.10-dev"
REQUIRED=false
check_executable
PYTHON310_AVAILABLE=$AVAILABLE

if [ "$PYTHON38_AVAILABLE" = "true" ]
then
  PYTHON=python3.8
elif [ "$PYTHON310_AVAILABLE" = "true" ]
then
  PYTHON=python3.10
else
  echo
  echo "Neither Python 3.8 nor Python 3.10 available!"
  echo "Install on Debian systems with:"
  echo "  sudo apt-get install python3.8 python3.8-dev"
  echo "or:"
  echo "  sudo apt-get install python3.10 python3.10-dev"
  echo
  exit 1
fi

REPO="ufdl-json-messages"
check_repository

REPO="ufdl-job-types"
check_repository

REPO="ufdl-job-contracts"
check_repository

#############
# EXECUTION #
#############

if [ "$PROMPT" = "yes" ]
then
  echo
  echo "Press any key to start setup of '$VENV' for running UFDL backend (using $PYTHON)..."
  read -s -n 1 key
fi

# update repos
if [ "$UPDATE" = "yes" ]
then
  REPO="ufdl-json-messages"
  update_repository

  REPO="ufdl-job-types"
  update_repository

  REPO="ufdl-job-contracts"
  update_repository

  echo "Updating this repo..."
  git pull
fi

# delete old directory
if [ -d "./$VENV" ]
then
  echo "Removing old virtual environment..."
  rm -rf ./$VENV
fi

# deleting old "build" directories
echo "Removing old 'build' directories..."
find . -type d -name build -exec rm -R {} \; 2>/dev/null
find ../ufdl-json-messages -type d -name build -exec rm -R {} \; 2>/dev/null
find ../ufdl-job-types -type d -name build -exec rm -R {} \; 2>/dev/null
find ../ufdl-job-contracts -type d -name build -exec rm -R {} \; 2>/dev/null

echo "Creating new virtual environment $VENV..."
virtualenv -p /usr/bin/$PYTHON ./$VENV

echo "Installing dependencies..."
./$VENV/bin/pip install --upgrade pip
./$VENV/bin/pip install --upgrade setuptools==59.4.0
./$VENV/bin/pip install Cython
./$VENV/bin/pip install numpy
./$VENV/bin/pip install "opencv-python<4.2.0"
# check for nvidia-smi and install GPU version
if [ -f "/usr/bin/nvidia-smi" ]
then
  ./$VENV/bin/pip install tensorflow-gpu
else
  ./$VENV/bin/pip install tensorflow
fi

echo "Installing UFDL modules..."
./$VENV/bin/pip install ../ufdl-json-messages/
./$VENV/bin/pip install ../ufdl-job-types/
./$VENV/bin/pip install ../ufdl-job-contracts/
./$VENV/bin/pip install ufdl-core-app/
./$VENV/bin/pip install ufdl-image-classification-app/
./$VENV/bin/pip install ufdl-image-segmentation-app/
./$VENV/bin/pip install ufdl-object-detection-app/
./$VENV/bin/pip install ufdl-spectrum-classification-app/
./$VENV/bin/pip install ufdl-speech-app/
./$VENV/bin/pip install ufdl-html-client-app/
./$VENV/bin/pip install ufdl-api-site/

if [ "$RESET" = "yes" ]
then
  echo "Configuring backend (admin/admin user)..."
  ./$VENV/bin/python -m ufdl.api_site.scripts.reset
fi

echo "Start dev server with:"
echo "  ./$VENV/bin/python -m ufdl.api_site.scripts.run [BIND]"
echo "Server is then running on:"
echo "  localhost:8000"
echo "Using '-b 0.0.0.0' as BIND address will make the server available on"
echo "port 8000 outside of localhost."
