# setup.py
# Copyright (C) 2020 Fracpete (fracpete at waikato dot ac dot nz)
from setuptools import setup, find_namespace_packages


setup(
    name="ufdl-api-site",
    description="The main Django site for UFDL server.",
    url="https://github.com/waikato-ufdl/ufdl-backend",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3',
    ],
    license='Apache License Version 2.0',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "ufdl"
    ],
    version="0.0.1",
    author='Corey Sterling',
    author_email='coreytsterling@gmail.com',
    install_requires=[
        "Django>=2.2.13,<3",
        "djangorestframework-simplejwt>=4.3.0,<5",
        "django-cors-headers>=3.2.1,<4",
        "ufdl-core-app",
        "ufdl-image-classification-app",
        "ufdl-object-detection-app",
        "ufdl-speech-app",
    ]
)
