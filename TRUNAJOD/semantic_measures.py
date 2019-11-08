#!/usr/bin/env python
# -*- coding: utf-8 -*-


def getSynsets(lemma, synset_dict):
    """
    Given a lemma, and a synset_dict, returns a set of all the synonyms
    for that lemma. If lemma not found in the synset_dict, it will return
    a set with the lemma.
    """
    return synset_dict.get(lemma, set([lemma]))


def overlap(lemma_list_group, synset_dict):
    """Computes average overlap in a text

    Computes semantic synset overlap (synonyms), based on a lemma list group
    and a dictionary containing synsets. Note that the computations are carried
    out dividing by number of text segments considered; matches TAACO
    implementation but not documentation. I will need to check why is this the
    case.

    Args:
        lemma_list_group (list) : A list of tokenized sentences.
        synset_dict (dict)      : A dictionary containing synsets.

    Returns:
        float: Average of overlaps between 2 sentences.
    """
    if len(lemma_list_group) < 2:
        return 0

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
    """
    Computes average semantic similarity between adjacent sentences, using
    SpaCy word2vec word vectors.
    """
    if N <= 1:
        return 0.0

    avg_sim = 0
    prev_doc = next(docs)

    done = False
    while not done:
        try:
            curr_doc = next(docs)
            avg_sim += prev_doc.similarity(curr_doc)
            prev_doc = curr_doc
        except StopIteration:
            done = True

    return avg_sim / float(N-1)
