from setuptools import setup, find_namespace_packages


setup(
    name="ufdl-html-client-app",
    description="HTML server for the UFDL web-client.",
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
        '': ['*.csv', '*.txt', '*.json', '*.html']
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
        "Django>=4.1,<5",
        "ufdl-core-app"
    ]
)
