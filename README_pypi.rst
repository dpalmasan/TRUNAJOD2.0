TRUNAJOD: A text complexity library for text analysis built on spaCy
====================================================================

``TRUNAJOD`` is a Python library for text complexity analysis build on the 
high-performance spaCy https://spacy.io/ library. With all the basic NLP capabilities provided by
spaCy (dependency parsing, POS tagging, tokenizing), `TRUNAJOD` focuses on extracting
measurements from texts that might be interesting for different applications and use cases.
Currently we only support Spanish.

.. image:: https://img.shields.io/github/v/release/dpalmasan/TRUNAJOD2.0   :alt: GitHub release (latest by date)

.. image:: https://img.shields.io/pypi/v/TRUNAJOD   :alt: PyPI


Features
========

* Utilities for text processing such as lemmatization, POS checkings.
* Semantic measurements from text such as average coherence between sentences and average synonym overlap.
* Giveness measurements such as pronoun density and pronoun noun ratio.
* Built-in emotion lexicon to compute emotion calculations based on words in the text.
* Lexico-semantic norm dataset to compute lexico-semantic variables from text.
* Type token ratio (TTR) based metrics, and tunnable TTR metrics.
* A built-in syllabizer (currently only for spanish).
* Discourse markers based measurements to obtain measures of connectivity inside the text.
* Plenty of surface proxies of text readability that can be computed directly from text.
* Measurements of parse tree similarity as an approximation to syntactic complexity.
* Parse tree correction to add periphrasis and heuristics for clause count, all based on linguistics experience.
* Entity Grid and entity graphs model implementation as a measure of coherence.
* An easy to use and user-friendly API.

Installation
============

To install the package:

``pip install TRUNAJOD``

Getting Started
===============

Using this package has some other pre-requisites. It assumes that you already have your model set up on spacy.
If not, please first install or download a model (for Spanish users, a spanish model). Then you can get started 
with the following code snippet.

You can download pre-build ``TRUNAJOD`` models from the repo, under the ``models`` directory.
Don´t forget to take a look at the documentation: https://trunajod20.readthedocs.io/en/latest.

For more examples, check the repo TRUNAJOD repo: https://github.com/dpalmasan/TRUNAJOD2.0.