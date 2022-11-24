#!/bin/bash

VENV="venv.dev"

if [ "$1" = "" ]
then
  echo "Use '-b 0.0.0.0' as first argument to make server available outside of localhost"
fi

./$VENV/bin/python -m ufdl.api_site.scripts.run $1
