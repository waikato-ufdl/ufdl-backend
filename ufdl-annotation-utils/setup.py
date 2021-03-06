# setup.py
# Copyright (C) 2020 Fracpete (fracpete at waikato dot ac dot nz)
from setuptools import setup, find_namespace_packages


setup(
    name="ufdl-annotation-utils",
    description="Tools for interoperating between UFDL and wai.annotations.",
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
        "wai.common>=0.0.35",
        "wai.json==0.0.5",
        "wai.annotations==0.6.0",
        "ufdl.json-messages"
    ]
)
