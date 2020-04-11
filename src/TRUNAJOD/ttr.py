#!/usr/bin/env python
"""Type Token Ratios module.

Type token ratios (TTR) are a measurement of lexical diversity. They are
defined as the ratio of unique tokens divided by the total number of tokens.
This measurement is bounded between 0 and 1. If there is no repetition in
the text this measurement is 1, and if there is infinite repetition, it will
tend to 0. This measurement is not recommended if analyzing texts of different
lengths, as when the number of tokens increases, the TTR tends flatten.
"""
from TRUNAJOD.utils import is_word


def type_token_ratio(word_list):
    """Return Type Token Ratio of a word list.

    :param word_list: List of words
    :type word_list: List of strings
    :return: TTR of the word list
    :rtype: float
    """
    return len(set(word_list)) / len(word_list)


def lexical_diversity_mtld(doc, ttr_segment=0.72):
    """Compute MTLD lexical diversity in a bi-directional fashion.

    :param doc: Processed text
    :type doc: Spacy Doc
    :return: Bi-directional lexical diversity MTLD
    :rtype: float
    """
    word_list = []
    for token in doc:
        if is_word(token.pos_):
            word_list.append(token.lemma_)
    return (one_side_lexical_diversity_mtld(word_list, ttr_segment) +
            one_side_lexical_diversity_mtld(word_list[::-1], ttr_segment)) / 2


def one_side_lexical_diversity_mtld(doc, ttr_segment=0.72):
    """Lexical diversity per MTLD.

    :param doc: Tokenized text
    :type doc: Spacy Doc
    :param ttr_segment: Threshold for TTR mean computation
    :type ttr_segment: float
    :return: MLTD lexical diversity
    :rtype: float
    """
    factor = 0
    total_words = 0
    non_ttr_segment = 1 - ttr_segment
    word_list = []
    for token in doc:
        word_list.append(token.lower())
        total_words += 1
        ttr = type_token_ratio(word_list)
        if ttr < ttr_segment:
            word_list = []
            factor += 1

    if word_list:
        factor += 1 - (
            type_token_ratio(word_list) - ttr_segment) / non_ttr_segment
        total_words += 1

    return total_words / factor
