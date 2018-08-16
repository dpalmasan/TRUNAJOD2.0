#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs

def flatten(list_of_lists):
    """
    Flattens a list of list. I use this for flattening list of lists of 
    tokens that are outputs of processing sentences.
    """
    return [item for sublist in list_of_lists for item in sublist]

def lemmatize(lemma_dict, word):
    """
    Lemmatizes a word using a lemmatizer which is represented as a dict that
    has (word, lemma) as (key, value) pair. For experiments, I will be using
    lemmas list from https://github.com/michmech/lemmatization-lists 

    If the word is not found in the dictionary, the lemma returned will be the 
    word with a * at the end.
    """
    return lemma_dict.get(word, word)

def getStopwords(filename):
    """
    Given a file with stopwords, generates a set from it and returns it.
    """
    stopwords = set([])
    with codecs.open(filename, "r", "utf8") as fp:
        for line in fp:
            word = line.strip()
            stopwords.add(word)

    return stopwords

def isStopword(word, stopwords):
    """
    Returns True if word in stopword list, false otherwise.
    """
    return word in stopwords

def readText(filename):
    with codecs.open(filename, "r", "utf8") as fp:
        text = fp.read()
    return text

def processText(text, sent_tokenize):
    """
    Processes text and returns sentences, paragraphs.
    """
    sentences = sent_tokenize(text)
    return sentences

def isNoun(pos_tag):
    """
    Returns True if pos_tag is NOUN, False otherwise.
    """
    return pos_tag == "PROPN" or pos_tag == "NOUN"

def isPronoun(pos_tag):
    """
    Returns True is pos_tag is PRON, False otherwise
    """
    return pos_tag == "PRON"

def isVerb(pos_tag):
    """
    Returns True if pos_tag is VERB, False otherwise.
    """
    return pos_tag == "VERB"

def isAdverb(pos_tag):
    """
    Returns True if pos_tag is ADV, False otherwise.
    """
    return pos_tag == "ADV"

def isAdjective(pos_tag):
    """
    Returns True if pos_tag is ADJ, False otherwise.
    """
    return pos_tag == "ADJ"

def isWord(pos_tag):
    return pos_tag != "PUNCT" and pos_tag != "SYM" and pos_tag != "SPACE"

def getTokenLemmas(doc, lemma_dict, stopwords=[]):
    """
    For a given doc, returns Noun and Verb Lemmas as lists.
    """
    noun_lemmas = []
    verb_lemmas = []
    content_lemmas = []
    function_lemmas = []
    adj_lemmas = []
    adv_lemmas = []
    prp_lemmas = []

    for token in doc:
        word = token.text.lower()
        word_lemma = lemmatize(lemma_dict, word)
        if isNoun(token.pos_):
            noun_lemmas.append(word_lemma)
        elif isVerb(token.pos_):
            verb_lemmas.append(word_lemma)
        elif isAdjective(token.pos_):
            adj_lemmas.append(word_lemma)
        elif isAdverb(token.pos_):
            adv_lemmas.append(word_lemma)
        elif isPronoun(token.pos_):
            prp_lemmas.append(word_lemma)

        if isStopword(word, stopwords):
            function_lemmas.append(word_lemma)
        else:
            if isWord(token.pos_):
                content_lemmas.append(word_lemma)




    return (noun_lemmas, verb_lemmas, function_lemmas, content_lemmas, 
            adj_lemmas, adv_lemmas, prp_lemmas)

def getSentencesLemmas(docs, lemma_dict, stopwords=[]):
    sentences_noun_lemmas = []
    sentences_verb_lemmas = []
    sentences_function_lemmas = []
    sentences_content_lemmas = []
    sentences_adj_lemmas = []
    sentences_adv_lemmas = []
    sentences_prp_lemmas = []

    for doc in docs:
        noun_lemmas, verb_lemmas, function_lemmas, content_lemmas, adj_lemmas, adv_lemmas, prp_lemmas = getTokenLemmas(doc, lemma_dict, stopwords)

        sentences_noun_lemmas.append(noun_lemmas)
        sentences_verb_lemmas.append(verb_lemmas)
        sentences_function_lemmas.append(function_lemmas)
        sentences_content_lemmas.append(content_lemmas)
        sentences_adj_lemmas.append(adj_lemmas)
        sentences_adv_lemmas.append(adv_lemmas)
        sentences_prp_lemmas.append(prp_lemmas)


    return (sentences_noun_lemmas, sentences_verb_lemmas, 
            sentences_function_lemmas, sentences_content_lemmas,
            sentences_adj_lemmas, sentences_adv_lemmas, sentences_prp_lemmas)
