"""
Setup script for TRUNAJOD.

This is the setup.py script for TRUNAJOD, to build and package TRUNAJOD.
"""
from distutils.core import setup

setup(
    name='TRUNAJOD',
    version='1.0',
    description='TRUNAJOD readability utilities',
    author='Diego Palma',
    author_email='dipalma@udec.cl',
    packages=['TRUNAJOD'],
    package_dir={'': 'src'})
