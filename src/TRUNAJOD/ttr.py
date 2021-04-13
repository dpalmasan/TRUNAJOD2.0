#!/usr/bin/env python
"""Type Token Ratios module.

Type token ratios (TTR) are a measurement of lexical diversity. They are
defined as the ratio of unique tokens divided by the total number of tokens.
This measurement is bounded between 0 and 1. If there is no repetition in
the text this measurement is 1, and if there is infinite repetition, it will
tend to 0. This measurement is not recommended if analyzing texts of different
lengths, as when the number of tokens increases, the TTR tends flatten.
"""
from collections import defaultdict
from typing import Dict
from typing import List

from spacy.tokens import Doc
from TRUNAJOD.utils import is_word
from TRUNAJOD.utils import SupportedModels


def type_token_ratio(word_list: List[str]) -> float:
    """Return Type Token Ratio of a word list.

    :param word_list: List of words
    :type word_list: List of strings
    :return: TTR of the word list
    :rtype: float
    """
    return len(set(word_list)) / len(word_list)


def lexical_diversity_mtld(
    doc: Doc, model_name: str = "spacy", ttr_segment: float = 0.72
) -> float:
    """Compute MTLD lexical diversity in a bi-directional fashion.

    :param doc: Processed text
    :type doc: NLP Doc
    :param model_name: Determines which model is used (spacy or stanza)
    :type model_name: str
    :param ttr_segment: Threshold for TTR mean computation
    :type ttr_segment: float
    :return: Bi-directional lexical diversity MTLD
    :rtype: float
    """
    # check model
    model = SupportedModels(model_name)

    word_list = []
    if model == SupportedModels.SPACY:
        for token in doc:
            if is_word(token.pos_):
                word_list.append(token.lemma_)
    elif model == SupportedModels.STANZA:
        for sent in doc.sentences:
            for word in sent.words:
                if is_word(word.upos):
                    word_list.append(word.lemma)
    return (
        one_side_lexical_diversity_mtld(word_list, model, ttr_segment)
        + one_side_lexical_diversity_mtld(word_list[::-1], model, ttr_segment)
    ) / 2


def one_side_lexical_diversity_mtld(
    doc: Doc, model_name: str = "spacy", ttr_segment: float = 0.72
) -> float:
    """Lexical diversity per MTLD.

    :param doc: Tokenized text
    :type doc: NLP Doc
    :param model_name: Determines which model is used (spacy or stanza)
    :type model_name: str
    :param ttr_segment: Threshold for TTR mean computation
    :type ttr_segment: float
    :return: MLTD lexical diversity
    :rtype: float
    """
    factor = 0
    total_words = 0
    non_ttr_segment = 1 - ttr_segment
    word_list = []

    # check model
    model = SupportedModels(model_name)

    if model == SupportedModels.SPACY or type(doc) == list:
        for token in doc:
            word_list.append(token.lower())
            total_words += 1
            ttr = type_token_ratio(word_list)
            if ttr < ttr_segment:
                word_list = []
                factor += 1
    elif model == SupportedModels.STANZA:
        if type(doc) != list:
            for sent in doc.sentences:
                for word in sent.words:
                    word_list.append(word.text.lower())
                    total_words += 1
                    ttr = type_token_ratio(word_list)
                    if ttr < ttr_segment:
                        word_list = []
                        factor += 1

    if word_list:
        factor += (
            1 - (type_token_ratio(word_list) - ttr_segment) / non_ttr_segment
        )
        total_words += 1
    return total_words / factor


def yule_k(doc: Doc) -> float:
    r"""Compute Yule's K from a text.

    Yule's K is defined as follows:

    .. math::
        K=10^{-4}\displaystyle\frac{\sum{r^2V_r-N}}{N^2}

    Where `Vr` is the number of tokens ocurring `r` times.
    This is a measurement of lexical diversity.

    :param doc: Processed spaCy Doc
    :type doc: Doc
    :return: Texts' Yule's K
    :rtype: float
    """
    counts: Dict[str, int] = defaultdict(int)
    N: int = 0
    for token in doc:
        if is_word(token.pos_):
            counts[token.lemma_] += 1
            N += 1

    rs: Dict[int, int] = defaultdict(int)
    for key, value in counts.items():
        rs[value] += 1

    return 1e-4 * sum(r ** 2 * vr - N for r, vr in rs.items()) / N ** 2
