# How to Install UFDL Backend

## Prerequisites

* Python 3.7
* Development headers (python3.7-dev) (Windows only?)
* Compiler e.g. gcc (exported as CC) (Windows only?)

## Checkout Source from Git

```
git clone https://github.com/waikato-ufdl/ufdl-backend.git
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
pip install ufdl-json-messages/
pip install ufdl-annotation-utils/
pip install ufdl-core-app/
pip install ufdl-image-classification-app/
pip install ufdl-object-detection-app/
pip install ufdl-api-site/
```

## Run the Reset Script to Create the Test Setup

Creates an admin user called "admin" with the password "admin".

```
python -m ufdl.api_site.scripts.reset
```

## Start the Server

```
python -m ufdl.api_site.scripts.manage runserver
```
