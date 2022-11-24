#!/bin/bash

VENV="venv.dev"

if [ ! "$1" = "-y" ]
then
  echo "Press any key to reset database of UFDL backend"
  read -s -n 1 key
fi

# check venv directory
if [ ! -d "./$VENV" ]
then
  echo "Virtual environment directory does not exist!"
  exit 1
fi

echo "Resetting DB..."
./$VENV/bin/python -m ufdl.api_site.scripts.reset

echo "Start dev server with:"
echo "  ./$VENV/bin/python -m ufdl.api_site.scripts.run [BIND]"
echo "Server is then running on:"
echo "  localhost:8000"
echo "Using '-b 0.0.0.0' as BIND address will make the server available on"
echo "port 8000 outside of localhost."
