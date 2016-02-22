"""Packaging settings."""


# Always prefer setuptools over distutils
from setuptools import Command, setup, find_packages
from codecs import open
from os import path
from dollop import __version__
from subprocess import call

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dollop',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    description='AWS EC2 Instance Creator',
    long_description=long_description,

    # The project's main homepage.
    url='TBD',

    author='Clay Smith',
    author_email='smithclay@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords='New Relic EC2 Instance Creator',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'tests']),

    install_requires=['troposphere'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
)
