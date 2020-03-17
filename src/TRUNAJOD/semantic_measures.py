#!/usr/bin/env python


def getSynsets(lemma, synset_dict):
    """Return synonym set given a word lemma.

    The function requires that the synset_dict is passed into it. In our case
    we extract the synset from MCR (Multilingual-Central-Repository). If the
    lemma is not found in the synset_dict, then this function returns a set
    with the lemma in it.

    :param lemma: Lemma to be look-up into the synset
    :type lemma: string
    :param synset_dict: key-value pairs, lemma to synset
    :type synset_dict: Python dict
    :return: The set of synonyms of a given lemma
    :rtype: Python set of strings
    """
    return synset_dict.get(lemma, {lemma})


def overlap(lemma_list_group, synset_dict):
    """Compute average overlap in a text.

    Computes semantic synset overlap (synonyms), based on a lemma list group
    and a dictionary containing synsets. Note that the computations are carried
    out dividing by number of text segments considered; matches TAACO
    implementation but not documentation. I will need to check why is this the
    case.

    :param lemma_list_group: List of tokenized and lemmatized sentences
    :type lemma_list_group: List of List of strings
    :param synset_dict: key-value pairs for lemma-synonyms
    :type synset_dict: Python dict
    :return: Average overlap between sentences
    :rtype: float
    """
    # TODO: Should this raise an exception?
    if len(lemma_list_group) < 2:
        return 0.0

    N = len(lemma_list_group)

    overlap_counter = 0
    for i in range(N-1):
        cur_list = set(lemma_list_group[i])
        next_list = set(lemma_list_group[i+1])
        for lemma in cur_list:
            for lemma_next in next_list:
                if lemma in getSynsets(lemma_next, synset_dict):
                    overlap_counter += 1

    # I got this from original TAACO code, it seems it is divided by the total
    # segments.
    return overlap_counter / float(N-1)


def avgW2VSemanticSimilarity(docs, N):
    """Compute average semantic similarity between adjacent sentences.

    This is using word2vec model based on SPACY implementation.

    :param docs: Docs generator provided by SPACY API
    :type docs: Doc Generator
    :param N: Number of sentences
    :type N: int
    :return: Average sentence similarity (cosine)
    :rtype: float
    """
    # TODO: Should this raise an exception?
    if N <= 1:
        return 0.0

    avg_sim = 0
    prev_doc = next(docs)

    # FIXME: Investiagte an alternative to this nasty implementation
    done = False
    while not done:
        try:
            curr_doc = next(docs)
            avg_sim += prev_doc.similarity(curr_doc)
            prev_doc = curr_doc
        except StopIteration:
            done = True

    return avg_sim / float(N-1)
