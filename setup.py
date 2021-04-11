"""
Setup script for TRUNAJOD.

This is the setup.py script for TRUNAJOD, to build and package TRUNAJOD.
"""
from distutils.core import setup


long_description = open("README.md", "r", encoding="utf-8").read()

setup(
    name="TRUNAJOD",
    version="0.1.1b",
    license="MIT",
    description="A python lib for readability analyses.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Diego Palma",
    author_email="dipalma@udec.cl",
    url="https://github.com/dpalmasan/TRUNAJOD2.0",
    download_url=(
        "https://github.com/dpalmasan/TRUNAJOD2.0/archive/refs/tags/v0.1.1.tar.gz"
    ),
    keywords=[
        "NLP",
        "readability",
        "entity grid",
        "linguistics",
        "nlp",
        "text complexity",
    ],
    packages=["TRUNAJOD"],
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        "spacy>=2.3.2",
    ],
    project_urls={
        "Documentation": "https://trunajod20.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/dpalmasan/TRUNAJOD2.0",
        "Bug Tracker": "https://github.com/dpalmasan/TRUNAJOD2.0/issues",
    },
    python_requires=">=3.6",
)
