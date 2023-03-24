# How to Install UFDL Backend

The script `dev_init.sh` performs all the steps outlined below
to set up a virtual environment.

## Prerequisites

See [Requirements section](README.md#requirements) in [README.md](README.md).

## Checkout Sources from Git

```
git clone https://github.com/waikato-ufdl/ufdl-backend.git
git clone https://github.com/waikato-ufdl/ufdl-json-messages.git
cd ufdl-backend
```

## Create a Virtual Environment

```
python3.7 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
```

## Install Specific Dependencies

The normal install will fail if these dependencies aren't installed first. This
is an on-going problem that will be addressed in future.

```
pip install Cython
pip install numpy
```

Tensorflow is required for wai-annotations (a dependency of UFDL):

```
pip install tensorflow
```
OR
```
pip install tensorflow-gpu
```

## Install the UFDL Packages

Order is important here.

```
pip install ../ufdl-json-messages/
pip install ufdl-annotation-utils/
pip install ufdl-core-app/
pip install ufdl-image-classification-app/
pip install ufdl-image-segmentation-app/
pip install ufdl-object-detection-app/
pip install ufdl-spectrum-classification-app/
pip install ufdl-speech-app/
pip install ufdl-api-site/
```

## Run the Reset Script to Create the Test Setup

Creates an admin user called "admin" with the password "admin".

```
python -m ufdl.api_site.scripts.reset
```

## Start the Server

```
python -m ufdl.api_site.scripts.manage runserver [BIND]
```

If `BIND` is omitted, the server runs on `localhost:8000`.
In order to expose the server on port 8000 outside of localhost, 
use `0.0.0.0:8000`. 
