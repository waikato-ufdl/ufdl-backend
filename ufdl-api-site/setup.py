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
    python_requires=">=3.8.0",
    install_requires=[
        "Django>=4.1,<5",
        "djangorestframework-simplejwt>=5.2,<6",
        "django-cors-headers>=3.13,<4",
        "psycopg2>=2.9,<3",
        "ufdl-core-app",
        "ufdl-html-client-app",
        "ufdl-image-classification-app",
        "ufdl-image-segmentation-app",
        "ufdl-object-detection-app",
        "ufdl-spectrum-classification-app",
        "ufdl-speech-app",
    ],
    entry_points={
        "console_scripts": [
            "ufdl-reset=ufdl.api_site.scripts.reset:reset",
            "ufdl-manage=ufdl.api_site.scripts.manage:main",
            "ufdl-run=ufdl.api_site.scripts.run:run"
        ]
    }
)
