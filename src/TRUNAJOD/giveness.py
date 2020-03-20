#!/usr/bin/env python
"""Giveness module."""
from TRUNAJOD.utils import isNoun
from TRUNAJOD.utils import isPronoun
from TRUNAJOD.utils import isWord

# Based on SPACY docs
THIRD_PERSON_LABEL = 'Person=3'


def pronounDensity(doc):
    """Compute pronoun density.

    This is a measurement of text complexity, in the sense that a text
    with a higher pronoun density will be more difficult to read than
    a text with lower pronoun density (due to inferences needed).

    :param doc: Document to be processed.
    :type doc: Spacy Doc
    :return: Pronoun density
    :rtype: float
    """
    word_counter = 0
    third_person_pronouns = 0
    for token in doc:
        if isWord(token.pos_):
            word_counter += 1
            if isPronoun(token.pos_) and THIRD_PERSON_LABEL in token.tag_:
                third_person_pronouns += 1

    return float(third_person_pronouns) / word_counter


def pronounNounRatio(doc):
    """Compute Pronoun Noun ratio.

    This is an approximation of text complexity/readability, since pronouns
    are co-references to a proper noun or a noun.

    :param doc: Text to be processed
    :type doc: Spacy doc
    :return: pronoun-noun ratio
    :rtype: float
    """
    noun_counter = 0
    third_person_pronouns = 0

    for token in doc:
        if isNoun(token.pos_):
            noun_counter += 1
        if isPronoun(token.pos_) and THIRD_PERSON_LABEL in token.tag_:
            third_person_pronouns += 1

    return float(third_person_pronouns) / noun_counter
