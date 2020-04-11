#!/usr/bin/env python
"""Givenness module.

Giveness is defined as the amount of given information a text exposes over
successive constituents :cite:`hempelmann2005using`. Givenness is can be used
as a proxy of text complexity.
"""
from TRUNAJOD.utils import is_noun
from TRUNAJOD.utils import is_pronoun
from TRUNAJOD.utils import is_word

# Based on SPACY docs
THIRD_PERSON_LABEL = 'Person=3'


def pronoun_density(doc):
    """Compute pronoun density.

    This is a measurement of text complexity, in the sense that a text
    with a higher pronoun density will be more difficult to read than
    a text with lower pronoun density (due to inferences needed). The
    way this is computed is taking the ratio between third person
    pronouns and total words in the text.

    :param doc: Document to be processed.
    :type doc: Spacy Doc
    :return: Pronoun density
    :rtype: float
    """
    word_counter = 0
    third_person_pronouns = 0
    for token in doc:
        if is_word(token.pos_):
            word_counter += 1
            if is_pronoun(token.pos_) and THIRD_PERSON_LABEL in token.tag_:
                third_person_pronouns += 1

    return float(third_person_pronouns) / word_counter


def pronoun_noun_ratio(doc):
    """Compute Pronoun Noun ratio.

    This is an approximation of text complexity/readability, since pronouns
    are co-references to a proper noun or a noun. This is computed as the
    taking the ratio between third person pronouns and total nouns.

    :param doc: Text to be processed
    :type doc: Spacy doc
    :return: pronoun-noun ratio
    :rtype: float
    """
    noun_counter = 0
    third_person_pronouns = 0

    for token in doc:
        if is_noun(token.pos_):
            noun_counter += 1
        if is_pronoun(token.pos_) and THIRD_PERSON_LABEL in token.tag_:
            third_person_pronouns += 1

    return float(third_person_pronouns) / noun_counter
