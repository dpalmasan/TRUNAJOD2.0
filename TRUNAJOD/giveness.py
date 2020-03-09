#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .utils import isWord
from .utils import isNoun
from .utils import isPronoun

# TODO: Do this in an object-oriented fashion. I should end up with a nice code
# and also, efficient, since all the computations can be done when creating the
# object instance, instead of repeating computations in the functions as it can
# be noted with the current approach


def pronounDensity(doc):
    """
    Given a SPACY doc, computes the pronoun density which is calculated as the
    number of third person pronouns divided by number of words.
    """
    word_counter = 0
    third_person_pronouns = 0
    for token in doc:
        if isWord(token.pos_):
            word_counter += 1
            if token.pos_ == "PRON" and "Person=3" in token.tag_:
                third_person_pronouns += 1

    return float(third_person_pronouns) / word_counter


# FIXME: I am not sure if I should consider Pronoun in noun counter.
def pronounNounRatio(doc):
    noun_counter = 0
    third_person_pronouns = 0

    for token in doc:
        if isNoun(token.pos_):
            noun_counter += 1
        if isPronoun(token.pos_) and "Person=3" in token.tag_:
            third_person_pronouns += 1

    return float(third_person_pronouns) / noun_counter
