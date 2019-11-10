from setuptools import setup


setup(
    name="ufdl-core-app",
    description="Core functionality for the UFDL API backend.",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    package_dir={
        '': 'src'
    },
    packages=["core"],
    version="0.0.1",
    author='Corey Sterling',
    author_email='coreytsterling@gmail.com',
    install_requires=[
        "django",
        "djangorestframework",
        "wai.common"
    ]
)
