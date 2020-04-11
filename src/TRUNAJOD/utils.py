#!/usr/bin/env python
"""Utility functions for TRUNAJOD library."""


def flatten(list_of_lists):
    """Flatten a list of list.

    This is a utility function that takes a list of lists and
    flattens it. For example the list ``[[1, 2, 3], [4, 5]]`` would be
    converted into ``[1, 2, 3, 4, 5]``.

    :param list_of_lists: List to be flattened
    :type list_of_lists: Python List of Lists
    :return: The list flattened
    :rtype: Python List
    """
    return [item for sublist in list_of_lists for item in sublist]


def get_sentences_lemmas(docs, lemma_dict, stopwords=[]):  # pragma: no cover
    """Get lemmas from sentences.

    Get different types of lemma measurements, such as noun lemmas, verb
    lemmas, content lemmas. It calls :func:`TRUNAJOD.utils.get_token_lemmas`
    internally to extract different lemma types for each sentence. This
    function extract the following lemmas:

    * Noun lemmas
    * Verb lemmas
    * Function lemmas (provided as ``stopwords``)
    * Content lemmas (anything that is not in ``stopwords``)
    * Adjective lemmas
    * Adverb lemmas
    * Proper pronoun lemmas

    :param docs: List of sentences to be processed.
    :type docs: List of Spacy Doc (Doc.sents)
    :param lemma_dict: Lemmatizer dictionary
    :type lemma_dict: dict
    :param stopwords: List of stopwords (function words), defaults to []
    :type stopwords: list, optional
    :return: List of lemmas from text
    :rtype: List of Lists of str
    """
    sentences_noun_lemmas = []
    sentences_verb_lemmas = []
    sentences_function_lemmas = []
    sentences_content_lemmas = []
    sentences_adj_lemmas = []
    sentences_adv_lemmas = []
    sentences_prp_lemmas = []

    for doc in docs:
        (
            noun_lemmas,
            verb_lemmas,
            function_lemmas,
            content_lemmas,
            adj_lemmas,
            adv_lemmas,
            prp_lemmas,
        ) = get_token_lemmas(doc, lemma_dict, stopwords)

        sentences_noun_lemmas.append(noun_lemmas)
        sentences_verb_lemmas.append(verb_lemmas)
        sentences_function_lemmas.append(function_lemmas)
        sentences_content_lemmas.append(content_lemmas)
        sentences_adj_lemmas.append(adj_lemmas)
        sentences_adv_lemmas.append(adv_lemmas)
        sentences_prp_lemmas.append(prp_lemmas)

    return (
        sentences_noun_lemmas,
        sentences_verb_lemmas,
        sentences_function_lemmas,
        sentences_content_lemmas,
        sentences_adj_lemmas,
        sentences_adv_lemmas,
        sentences_prp_lemmas,
    )


def get_stopwords(filename):
    """Read stopword list from file.

    Assumes that the list is defined as a newline separated words. It is
    a utility in case you'd like to provide your own stopwords list.
    Assumes encoding ``utf8``.

    :param filename: Name of the file containing stopword list.
    :type filename: string
    :return: List of stopwords
    :rtype: set
    """
    stopwords = set()
    with open(filename, 'r', encoding='utf8') as fp:
        for line in fp:
            word = line.strip()
            stopwords.add(word)

    return stopwords


def get_token_lemmas(doc, lemma_dict, stopwords=[]):  # pragma: no cover
    """Return lemmas from a sentence.

    From a sentence, extracts the following lemmas:

    * Noun lemmas
    * Verb lemmas
    * Function lemmas (provided as ``stopwords``)
    * Content lemmas (anything that is not in ``stopwords``)
    * Adjective lemmas
    * Adverb lemmas
    * Proper pronoun lemmas

    :param doc: Doc containing tokens from text
    :type doc: Spacy Doc
    :param lemma_dict: Lemmatizer key-value pairs
    :type lemma_dict: Dict
    :param stopwords: list of stopwords, defaults to []
    :type stopwords: set/list, optional
    :return: All lemmas for noun, verb, etc.
    :rtype: tuple of lists
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
        if is_noun(token.pos_):
            noun_lemmas.append(word_lemma)
        elif is_verb(token.pos_):
            verb_lemmas.append(word_lemma)
        elif is_adjective(token.pos_):
            adj_lemmas.append(word_lemma)
        elif is_adverb(token.pos_):
            adv_lemmas.append(word_lemma)
        elif is_pronoun(token.pos_):
            prp_lemmas.append(word_lemma)

        if is_stopword(word, stopwords):
            function_lemmas.append(word_lemma)
        else:
            if is_word(token.pos_):
                content_lemmas.append(word_lemma)

    return (
        noun_lemmas,
        verb_lemmas,
        function_lemmas,
        content_lemmas,
        adj_lemmas,
        adv_lemmas,
        prp_lemmas,
    )


def is_adjective(pos_tag):
    """Return ``True`` if ``pos_tag`` is ``ADJ``, False otherwise.

    :param pos_tag: Part of Speech tag
    :type pos_tag: string
    :return: True if POS is adjective
    :rtype: boolean
    """
    return pos_tag == 'ADJ'


def is_adverb(pos_tag):
    """Return ``True`` if ``pos_tag`` is ``ADV``, False otherwise.

    :param pos_tag: Part of Speech tag
    :type pos_tag: string
    :return: True if POS is adverb
    :rtype: boolean
    """
    return pos_tag == 'ADV'


def is_noun(pos_tag):
    """Return ``True`` if ``pos_tag`` is ``NOUN`` or ``PROPN``, False otherwise.

    :param pos_tag: Part of Speech tag
    :type pos_tag: string
    :return: True if POS is noun or proper noun
    :rtype: boolean
    """
    return pos_tag == 'PROPN' or pos_tag == 'NOUN'


def is_pronoun(pos_tag):
    """Return ``True`` if ``pos_tag`` is ``PRON``, False otherwise.

    :param pos_tag: Part of Speech tag
    :type pos_tag: string
    :return: True if POS is pronoun
    :rtype: boolean
    """
    return pos_tag == 'PRON'


def is_stopword(word, stopwords):
    """Return ``True`` if ``word`` is in ``stopwords``, False otherwise.

    :param word: Word to be checked
    :type word: string
    :param stopwords: stopword list
    :type stopwords: List of strings
    :return: True if word in stopwords
    :rtype: boolean
    """
    return word in stopwords


def is_verb(pos_tag):
    """Return ``True`` if ``pos_tag`` is ``VERB``, False otherwise.

    :param pos_tag: Part of Speech tag
    :type pos_tag: string
    :return: True if POS is verb
    :rtype: boolean
    """
    return pos_tag == 'VERB'


def is_word(pos_tag):
    """Return ``True`` if ``pos_tag`` is not punctuation, False otherwise.

    This method checks that the ``pos_tag`` does not belong to the following
    set: ``{'PUNCT', 'SYM', 'SPACE'}``.

    :param pos_tag: Part of Speech tag
    :type pos_tag: string
    :return: True if POS is a word
    :rtype: boolean
    """
    return pos_tag != 'PUNCT' and pos_tag != 'SYM' and pos_tag != 'SPACE'


def lemmatize(lemma_dict, word):
    """Lemmatize a word.

    Lemmatizes a word using a lemmatizer which is represented as a dict that
    has (word, lemma) as (key, value) pair. An example of a lemma list can be
    found in https://github.com/michmech/lemmatization-lists.

    If the word is not found in the dictionary, the lemma returned will be the
    word.

    :param lemma_dict: A dict (word, lemma)
    :type lemma_dict: Python dict
    :param word: The word to be lemmatized
    :type word: string
    :return: Lemmatized word
    :rtype: string
    """
    return lemma_dict.get(word, word)


def process_text(text, sent_tokenize):
    """Process text by tokenizing sentences given a tokenizer.

    :param text: Text to be processed
    :type text: string
    :param sent_tokenize: Tokenizer
    :type sent_tokenize: Python callable that returns list of strings
    :return: Tokenized sentences
    :rtype: List of strings
    """
    return sent_tokenize(text)


def read_text(filename):
    """Read a ``utf-8`` encoded text file and returns the text as ``string``.

    This is just a utily function, that is not recommended to use if the text
    file does not fit your available RAM. Mostly used for small text files.

    :param filename: File from which is the text to be read
    :type filename: string
    :return: Text in the file
    :rtype: string
    """
    with open(filename, 'r', encoding='utf8') as fp:
        text = fp.read()
    return text
