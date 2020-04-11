"""
Setup script for TRUNAJOD.

This is the setup.py script for TRUNAJOD, to build and package TRUNAJOD.
"""
from distutils.core import setup

setup(
    name='TRUNAJOD',
    version='0.1',
    license='MIT',
    description='TRUNAJOD readability library for Python',
    author='Diego Palma',
    author_email='dipalma@udec.cl',
    url="https://github.com/dpalmasan/TRUNAJOD2.0",
    download_url=(
        "https://github.com/dpalmasan/TRUNAJOD2.0/archive/v0.1.tar.gz"),
    keywords=[
        "NLP", "readability", "entity grid", "linguistics", "computational",
        "spacy"
    ],
    packages=['TRUNAJOD'],
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ])
