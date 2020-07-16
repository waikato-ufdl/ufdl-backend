#!/bin/bash

echo "Press any key to reset database of UFDL backend"
read -s -n 1 key

# check venv directory
if [ ! -d "./venv.dev" ]
then
  echo "Virtual environment directory does not exist!"
  exit 1
fi

echo "Resetting DB..."
./venv.dev/bin/python -m ufdl.api_site.scripts.reset

echo "Start dev server with:"
echo "./venv.dev/bin/python -m ufdl.api_site.scripts.manage runserver"

echo "Server is running on:"
echo "localhost:8000"
