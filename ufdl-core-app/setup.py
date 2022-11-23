from setuptools import setup, find_namespace_packages


setup(
    name="ufdl-core-app",
    description="Core functionality for the UFDL API backend.",
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
    package_data={
        '': ['*.csv', '*.txt', '*.json']
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "ufdl"
    ],
    include_package_data=True,
    version="0.0.1",
    author='Corey Sterling',
    author_email='coreytsterling@gmail.com',
    python_requires="==3.8.*",
    install_requires=[
        "wai.json==0.0.5",
        "Django>=4.1,<5",
        "djangorestframework>=3.14,<4",
        "simple-django-teams==0.0.6",
        "ufdl.json-messages",
        "requests-file>=1.5,<1.6",
        "channels>=3,<4",
        "channels_redis>=4,<5",
        "ufdl.jobtypes",
        "ufdl.jobcontracts",
        "wai.lazypip"
    ]
)
