#!/usr/bin/env python
"""Type Token Ratios module.

Type token ratios (TTR) are a measurement of lexical diversity. They are
defined as the ratio of unique tokens divided by the total number of tokens.
This measurement is bounded between 0 and 1. If there is no repetition in
the text this measurement is 1, and if there is infinite repetition, it will
tend to 0. This measurement is not recommended if analyzing texts of different
lengths, as when the number of tokens increases, the TTR tends flatten.
"""
import math
from collections import defaultdict
from typing import Dict
from typing import List

import numpy as np
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
    for token in doc:
        if is_word(token):
            word_list.append(token.lemma_)
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

    Yule's K is defined as follows :cite:`yule2014statistical`:

    .. math::
        K=10^{4}\displaystyle\frac{\sum{r^2V_r-N}}{N^2}

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
        if is_word(token):
            counts[token.lemma_] += 1
            N += 1

    rs: Dict[int, int] = defaultdict(int)
    for key, value in counts.items():
        rs[value] += 1

    return 1e4 * sum(r ** 2 * vr - N for r, vr in rs.items()) / N ** 2


def d_estimate(
    doc: Doc, min_range: int = 35, max_range: int = 50, trials: int = 5
) -> float:
    r"""Compute D measurement for lexical diversity.

    The measurement is based in :cite:`richards2000measuring`. We pick ``n``
    numbers of tokens, varying ``N`` from ``min_range`` up to ``max_range``.
    For each ``n`` we do the following:

    1. Sample ``n`` tokens without replacement
    2. Compute ``TTR``
    3. Repeat steps 1 and 2 ``trials`` times
    4. Compute the average ``TTR``

    At this point, we have a set of points ``(n, ttr)``. We then fit
    these observations to the following model:

    .. math::
        TTR = \displaystyle\frac{D}{N}\left[\sqrt{1 + 2\frac{N}{D}} - 1\right]

    The fit is done to get an estimation for the ``D`` parameter, and we use
    a least squares as the criteria for the fit.

    :param doc: SpaCy doc of the text.
    :type doc: Doc
    :param min_range: Lower bound for n, defaults to 35
    :type min_range: int, optional
    :param max_range: Upper bound for n, defaults to 50
    :type max_range: int, optional
    :param trials: Number of trials to estimate TTR, defaults to 5
    :type trials: int, optional
    :raises ValueError: If invalid range is provided.
    :return: D metric
    :rtype: float
    """
    if min_range >= max_range:
        raise ValueError(
            "max_range should be greater than min_range"
            f"you provided [{min_range}, {max_range}]"
        )
    token_list: List[str] = []
    for token in doc:
        if is_word(token):
            token_list.append(token.lemma_)

    ns = np.arange(min_range, max_range + 1)
    ttrs = np.zeros(len(ns))
    for idx, sample_size in enumerate(ns):
        ttr = 0
        for trial in range(trials):
            word_list = np.random.choice(
                token_list, sample_size, replace=False
            )
            ttr += type_token_ratio(word_list)
        ttrs[idx] = ttr / trials
    A = np.vstack([2 * (1 - ttrs) / ns]).T
    y = ttrs ** 2
    d = np.linalg.lstsq(A, y, rcond=None)[0]
    return d[0]


def guirauds_index(doc: Doc) -> float:
    """Compute Guiraud's Index from a text.

    Yule's K is defined as follows:

    .. math::
        GI = V / Squarert(N)

    Where 'V' is the number of distinct words and 'N' is the total number of words.

    :param doc: Processed spaCy Doc
    :type doc: Doc
    :return: Texts' Guiraud's Index
    :rtype: float
    """
    word_counter = 0
    words = {}
    for token in doc:
        if is_word(token.pos_):
            word_counter += 1
            if token not in words:
                words[str(token)] = ""

    return len(words) / math.sqrt(word_counter)


def word_variation_index(doc: Doc) -> float:
    r"""Compute Word Variation Index.

    Word variation index might be thought as the density
    of ideas in a text. It is computed as:

    .. math::
        WVI = \displaystyle\frac{log\left(n(w)\right)}
        {log\left(2 - \frac{log(n(vw))}{log(n(w))}\right)}

    Where `n(w)` is the number of words in the text, and `n(vw)` is
    the number of unique words in the text.

    :param doc: Document to be processed
    :type doc: Doc
    :return: Word variation index
    :rtype: float
    """
    token_list: List[str] = []
    for token in doc:
        if is_word(token):
            token_list.append(token.lemma_)

    number_of_words = len(token_list)
    number_of_types = len(set(token_list))
    return np.log(number_of_words) / np.log(
        2 - np.log(number_of_types) / np.log(number_of_words)
    )
