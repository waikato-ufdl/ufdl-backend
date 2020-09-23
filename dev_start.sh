#!/bin/bash

VENV="venv.dev"

if [ "$1" = "" ]
then
  echo "Starting dev server on localhost:8000"
  echo "Use '0.0.0.0:8000' as first argument to make server available outside of localhost"
else
  echo "Starting dev server on $1"
fi

./$VENV/bin/python -m ufdl.api_site.scripts.manage runserver $1
