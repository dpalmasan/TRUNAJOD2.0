#!/usr/bin/env python
"""
Surface proxies of TRUNAJOD.

These surface proxies are measurements from text that consists on shallow
measures (proxies) that approximate to intrinsic properties of the text such
as cohesion, coherence, complexity. Examples of these measurements include but
are not limited to: Number of sentences, number of syllables, etc.
"""
import re
from copy import deepcopy
from functools import wraps
from math import log

from TRUNAJOD.syllabizer import Syllabizer
from TRUNAJOD.utils import is_word
from TRUNAJOD.verb_types import GERUND_VERBS
from TRUNAJOD.verb_types import INFINITIVE_VERBS
from TRUNAJOD.verb_types import PAST_TENSE_VERBS

PERIPHRASIS_GER = 'VerbForm=Ger'
PERIPHRASIS_INF = 'VerbForm=Inf'
PERIPHRASIS_PAR = 'VerbForm=Part'
PERIPHRASIS_SUF = "|Perif"

NEGATION_WORDS = {
    "no", "ni", "nunca", "jamás", "jamás", "tampoco", "nadie", "nada",
    "ningún", "ninguno", "ninguna"
}


def _fix_doc(func):
    @wraps(func)
    def function_wrapper(doc, infinitive_map):
        fixed_doc = fix_parse_tree(doc, infinitive_map)
        return func(fixed_doc, infinitive_map)

    return function_wrapper


def add_periphrasis(doc, periphrasis_type, periphrasis_list):
    """Add periphrasis to SPACY tags.

    One of the drawbacks that spaCy has, is that it does not address properly
    periphrasis of texts (in our case Spanish text). This function adds
    periphrasis to the text in order to improve further analysis such as
    clause segmentation, and clause count. This is used by
    :func:`TRUNAJOD.surface_proxies.fix_parse_tree`.

    :param doc: Tokenized text
    :type doc: Spacy Doc
    :param type: Periphrasis type
    :type type: string
    :param periphrasis_list: List of periphrasis
    :type periphrasis_list: List of strings
    :return: Corrected doc
    :rtype: Spacy Doc
    """
    regexp = re.compile(periphrasis_type)
    for token in doc:
        if token.pos_ in {"VERB", "AUX"} or regexp.search(token.tag_):
            if regexp.search(token.tag_):
                for periphrasis in periphrasis_list:
                    # For multi-word periphrases
                    periphrasis_words = periphrasis.split()
                    pos = token.i - len(periphrasis_words)
                    if (pos >= 0):
                        fail = False
                        for word in periphrasis_words:
                            if word.lower() != doc[pos].lemma_:
                                fail = True
                                break
                            pos = pos + 1
                        if not fail:
                            pos = token.i - len(periphrasis_words) + 1
                            for k in range(len(periphrasis_words)):
                                doc[pos].tag_ = doc[pos].tag_ + PERIPHRASIS_SUF
                                pos = pos + 1
    return doc


def average_clause_length(doc, infinitive_map):
    """Return average clause length (heuristic).

    This measurement is computed as the ratio of # of words / # of clauses.
    To count clauses we do it heuristically, and you can refer to
    :func:`TRUNAJOD.surface_proxies.clause_count` for more details.

    :param doc: Text to be processed
    :type doc: Spacy Doc
    :param infinitve_map: Lexicon containing maps from conjugate to infinitive.
    :type infinitive_map: dict
    :return: Average clause length
    :rtype: float
    """
    return word_count(doc) / clause_count(doc, infinitive_map)


def average_sentence_length(doc):
    """Return average sentence length.

    This measurement is computed as the ratio of: # of words / # of sentences.

    :param doc: Text to be processed.
    :type doc: Spacy Doc
    :return: average sentence length
    :rtype: float
    """
    return word_count(doc) / sentence_count(doc)


def average_word_length(doc):
    """Return average word length.

    Computed as the ratio of: # number of chars / # of words

    :param doc: Text to be processed.
    :type doc: Spacy Doc
    :return: Average word length
    :rtype: float
    """
    return char_count(doc) / word_count(doc)


def char_count(doc):
    """Return number of chars in a text.

    This count does not consider anything that its ``Token.pos_`` tag is
    either ``PUNCT`` or ``SPACE``.

    :param doc: Text to be processed.
    :type doc: Spacy Doc
    :return: Char count
    :rtype: int
    """
    return sum([
        len(token.lower_) for token in doc
        if token.pos_ not in {"PUNCT", "SPACE"}
    ])


@_fix_doc
def clause_count(doc, infinitive_map):
    """Return clause count (heuristic).

    This function is decorated by the
    :func:`TRUNAJOD:surface_proxies.fix_parse_tree` function, in order to
    heuristically count clauses.

    :param doc: Text to be processed.
    :type doc: Spacy Doc
    :param infinitve_map: Lexicon containing maps from conjugate to infinitive.
    :type infinitive_map: dict
    :return: Clause count
    :rtype: int
    """
    n_clauses = 0
    regexp = re.compile('VerbForm=Fin')
    regexp_perif = re.compile("Perif")
    for token in doc:
        verb_or_aux = token.pos_ in {"VERB", "AUX"}
        if verb_or_aux and not regexp_perif.search(token.tag_):
            if regexp.search(token.tag_):
                n_clauses += 1
    return n_clauses


def first_second_person_count(doc):
    """Count first|second person tokens.

    :param doc: Processed text
    :type doc: Spacy Doc
    :return: First and second person count
    :rtype: int
    """
    criteria = re.compile('Person=1|Person=2')
    return sum([1 for token in doc if criteria.search(token.tag_)])


def first_second_person_density(doc):
    """Compute density of first|second person.

    :param doc: Processed text
    :type doc: Spacy Doc
    :return: Density 1,2 person
    :rtype: float
    """
    return first_second_person_count(doc) / word_count(doc)


def fix_parse_tree(doc, infinitive_map):
    """Fix SPACY parse tree.

    We found that for Spanish texts, spaCy tags do not deal appropiately
    with periphrasis and other lingüistic cues. This function address this
    shortcome by modifying the parse tree computed by spaCy adding
    periphrasis for Gerunds, Infinitive and  Past tense verbs.

    :param doc: Processed text
    :type doc: Spacy Doc
    :param infinitve_map: Lexicon containing maps from conjugate to infinitive.
    :type infinitive_map: dict
    :return: Fixed Doc
    :rtype: Spacy Doc
    """
    fixed_doc = deepcopy(doc)
    for token in fixed_doc:
        if token.pos_ in {"VERB", "AUX"}:
            conjugate = infinitve(token.text, infinitive_map)
            if conjugate is not None:
                token.lemma_ = conjugate
    fixed_doc = add_periphrasis(fixed_doc, PERIPHRASIS_INF, INFINITIVE_VERBS)
    fixed_doc = add_periphrasis(fixed_doc, PERIPHRASIS_GER, GERUND_VERBS)
    fixed_doc = add_periphrasis(fixed_doc, PERIPHRASIS_PAR, PAST_TENSE_VERBS)
    return fixed_doc


def frequency_index(doc, frequency_dict):
    """Return frequency index.

    The frequency index is defined as the average frequency of the rarest
    word over sentences. To compute this, we use a dictionary. In the case
    of this Spanish implementation we could use RAE dictionary CREA.

    :param doc: Tokenized text.
    :type doc: Spacy Doc
    :return: Frequency index
    :rtype: float
    """
    n_sents = 0
    aggregate_frec = 0
    for sent in doc.sents:
        minimum = 99999999999999
        for token in sent:
            if is_word(token.pos_):
                frec = frequency_dict.get(token.lower_, 0)
                if frec < minimum and frec > 0:
                    minimum = frec
        if minimum > 0:
            aggregate_frec += log(minimum, 10)
            n_sents += 1
    return aggregate_frec / n_sents


def get_word_depth(index, doc):
    """Get word depth in the parse tree given a sentence and token index.

    The ``ROOT`` of the sentence is considered level 1. This method traverses
    the parse tree until reaching the ``ROOT``, and counts all levels
    traversed.

    :param index: Position of the token in the sentence
    :type index: int
    :param doc: Tokenized text
    :type doc: Spacy Doc
    :return: Depth of the of the token
    :rtype: int
    """
    token = doc[index]
    token_parent = doc[index].head
    depth = 1
    while token != token_parent:
        token = token.head
        token_parent = token_parent.head
        depth += 1
    return depth


def infinitve(conjugate, infinitive_map):
    """Get infinitive form of a conjugated verb.

    Given a mapping of conjugate to infinitive, this function computes
    the infinitive form of a conjugate verb. We provide models available
    for downloading, so you do not have to worry about the ``infinitive_map``.
    Regretfully we only provide models for Spanish texts.

    :param conjugate: Verb to be processed
    :type conjugate: string
    :param infinitve_map: Lexicon containing maps from conjugate to infinitive.
    :type infinitive_map: dict
    :return: Infinitive form of the verb, None if not found
    :rtype: string
    """
    conjugate = conjugate.lower()
    for word_list in infinitive_map:
        if conjugate in word_list:
            infinitive = infinitive_map[word_list]
            return infinitive if infinitive else None
    return None


def lexical_density(doc):
    """Compute lexical density.

    The lexical density is defined as the Part of Speech ratio of the
    following tags: ``VERB``, ``AUX``, ``ADJ``, ``NOUN``, ``PROPN`` and
    ``ADV`` over the total number of words.

    :param doc: Tokenized text
    :type doc: Spacy Doc
    :return: Lexical density
    :rtype: Float
    """
    return pos_ratio(doc, "VERB|AUX|ADJ|NOUN|PROPN|ADV")


def connection_words_ratio(doc):
    """Get ratio of connecting words over total words of text.

    This function computes the ratio of connective words over the total
    number of words. This implementation is only supported in Spanish and
    we consider the following lemmas: ``y``, ``o``, ``no``, ``si``.

    :param doc: Tokenized text
    :type doc: Spacy Doc
    :return: Connection word ratio
    :rtype: float
    """
    return sum([
        1 for token in doc if token.lemma_.lower() in {"y", "o", "no", "si"}
        and is_word(token.pos_)
    ]) / word_count(doc)


def negation_density(doc):
    """Compute negation density.

    This is defined as the ratio between number of occurrences of
    ``TRUNAJOD.surface_proxies.NEGATION_WORDS`` in the text over the
    total word count.

    :param doc: Tokenized text
    :type doc: Spacy Doc
    :return: Negation density
    :rtype: float
    """
    negation_count = 0
    for token in doc:
        if is_word(token.pos_) and token.lemma_.lower() in NEGATION_WORDS:
            negation_count += 1

    return negation_count / word_count(doc)


def node_similarity(node1, node2, is_central_node=False):
    """Compute node similarity recursively, based on common children POS.

    This function is called inside
    :func:`TRUNAJOD.surface_proxies.syntactic_similarity`
    so is an auxiliary function. In the common use case, is unlikely you will
    need to call this function directly, but we provide it for debugging
    purposes.

    :param node1: Node of the parse tree.
    :type node1: Spacy Token
    :param node2: Node of the parse tree
    :type node2: Spacy Token
    :param is_central_node: Whether is the central node, defaults to False
    :type is_central_node: bool, optional
    :return: Total childs in common between node1 and node2.
    :rtype: int
    """
    similarity = 0
    common_childs_node1 = set()
    common_childs_node2 = set()
    if is_central_node:
        if node1.pos_ == node2.pos_:
            similarity += 1
        else:
            return 0

    for child1 in node1.children:
        for child2 in node2.children:
            child_not_seen = child1 not in common_childs_node1\
                and child2 not in common_childs_node2
            if child1.pos_ == child2.pos_ and child_not_seen:
                similarity += 1
                common_childs_node1.add(child1)
                common_childs_node2.add(child2)
                similarity +=\
                    node_similarity(child1, child2, False)

    return similarity


def noun_count(doc):
    """Count nouns in the text.

    Count all tokens which Part of Speech tag is either ``NOUN`` or
    ``PROPN``.

    :param doc: Text to be processed
    :type doc: Spacy Doc
    :return: Noun count
    :rtype: int
    """
    return sum([1 for token in doc if token.pos_ in {"NOUN", "PROPN"}])


def noun_phrase_density(doc):
    """Compute NP density.

    To compute NP density we do it heuristically. We might improve it in the
    future by using some NP-chunking strategy. For counting noun phrases, we
    check that for a node in the parse tree, its head is a Noun. Then, we
    check if either of the following conditions is met:

    * The token is the article ``del`` or ``al``
    * The token dependency is not ``cc``, ``case`` or ``cop``, and the token
      is not a punctuation and the token is not the ``ROOT``

    Then we compute the ratio between # of NP / Noun count.

    :param doc: Tokenized text.
    :type doc: Spacy Doc
    :return: NP density
    :rtype: float
    """
    children = 0
    for sent in doc.sents:
        for token in sent:
            if token.head.pos_ in {"NOUN", "PROPN"}:
                spanish_al_del_article = token.text.upper() in {"AL", "DEL"}
                condition = token.dep_ not in {"cc", "case", "cop"}
                condition = condition and token.pos_ != "PUNCT"
                condition = condition and token.head != token
                if spanish_al_del_article or condition:
                    children += 1

    return children / noun_count(doc)


def pos_dissimilarity(doc):
    """Measure Part of Speech disimilarity over sentences.

    The dissimilarity of POS between two sentences is the difference
    between POS distribution over the total population of POS tags.
    It is computed as follows:

    * For each sentence, PoS tag distribution is computed.
    * For each tag in either of the two sentences, we compute the difference
      in distributions (absolute value)
    * This difference is divided by the total population of the sentences

    This is done for each pair of sentences (``N - 1`` sentences) and the
    results are averaged (again, over ``N - 1``)

    :param doc: Processed text
    :type doc: Spacy Doc
    :return: Part of Speech dissimilarity
    :rtype: float
    """
    sent_pos_dist = []
    for sent in doc.sents:
        sent_pos_dist.append(pos_distribution(sent))

    disimilarity = 0
    for i in range(len(sent_pos_dist) - 1):
        common_adj_tags = set(sent_pos_dist[i].keys())\
            | set(sent_pos_dist[i + 1].keys())
        difference = 0
        totals = 0
        for pos in common_adj_tags:
            pos_dist_value = sent_pos_dist[i].get(pos, 0)
            pos_dist_value_next = sent_pos_dist[i + 1].get(pos, 0)

            difference += abs(pos_dist_value - pos_dist_value_next)
            totals += pos_dist_value + pos_dist_value_next

        disimilarity += difference / totals
    return disimilarity / (len(sent_pos_dist) - 1)


def pos_distribution(doc):
    """Get POS distribution from a processed text.

    Let us suppose that a given sentence has the following pos tags:
    ``[NOUN, VERB, ADJ, VERB, ADJ]``. The PoS distribution would be

    * ``NOUN: 1``
    * ``VERB: 2``
    * ``ADJ: 2``

    This function returns this distrubution as a dict.

    :param doc: Processed text
    :type doc: Spacy Doc
    :return: POS distribution as a dict key POS, value Count
    :rtype: dict
    """
    distribution = {}
    for token in doc:
        distribution[token.pos_] = distribution.get(token.pos_, 0) + 1
    return distribution


def pos_ratio(doc, pos_types):
    """Compute POS ratio given desired type of ratio.

    The ``pos_types`` might be a regular expression if a composed ratio
    is needed. An example of usage would be ``pos_ratio(doc, "VERB|AUX")``.

    :param doc: Spacy processed text
    :type doc: Spacy Doc
    :param pos_types: POS to get the ratio
    :type pos_types: string
    :return: Ratio over number of words
    :rtype: float
    """
    pos_regex = re.compile(pos_types)
    total_words = 0
    total_pos_tags = 0
    for token in doc:
        if is_word(token.pos_):
            total_words += 1
            if pos_regex.search(token.tag_):
                total_pos_tags += 1
    return total_pos_tags / total_words


def sentence_count(doc):
    """Return number of sentences in a text.

    :param doc: Text to be processed
    :type doc: Spacy Doc
    :return: Number of sentences in the text
    :rtype: int
    """
    return len(list(doc.sents))


def syllable_count(doc):
    """Return number of syllables of a text.

    :param doc: Text to be processed.
    :type doc: Spacy Doc
    :return: Number of syllables in the text
    :rtype: int
    """
    return sum([
        Syllabizer.number_of_syllables(token.lower_) for token in doc
        if token.pos_ != "PUNCT"
    ])


def syntactic_similarity(doc):
    """Compute average syntactic similarity between sentences.

    For each pair of sentences, compute the similarity between each
    pair of nodes, using :func:`TRUNAJOD.surface_proxies.node_similarity`
    Then, the result is averaged over the ``N - 1`` pair of sentences.

    :param doc: Processed text
    :type doc: Spacy Doc
    :return: Average syntactic similarity over sentences.
    :rtype: float
    """
    n_sentences = 0
    prev_sent = None
    aggregate_similarity = 0
    for sent in doc.sents:
        n_sentences += 1
        if prev_sent is not None:
            common_nodes = node_similarity(sent.root, prev_sent.root, True)
            aggregate_similarity += common_nodes\
                / (len(sent) + len(prev_sent) - common_nodes)
        prev_sent = sent
    return aggregate_similarity / (n_sentences - 1)


def syllable_word_ratio(doc):
    """Return average syllable word ratio.

    It is computed as # Syllables / # of words.

    :param doc: Text to be processed.
    :type doc: Spacy Doc
    :return: syllable word ratio
    :rtype: float
    """
    return syllable_count(doc) / word_count(doc)


def subordination(doc, infinitive_map):
    """Return subordination, defined as the clause density.

    The subordination is defined as the ratio between # of clauses and
    the # of sentences. To compute number of clauses, a heuristic is used.

    :param doc: Text to be processed.
    :type doc: Spacy Doc
    :param infinitve_map: Lexicon containing maps from conjugate to infinitive.
    :type infinitive_map: dict
    :return: Subordination index
    :rtype: float
    """
    return clause_count(doc, infinitive_map) / sentence_count(doc)


def verb_noun_ratio(doc):
    """Compute Verb/Noun ratio.

    :param doc: Processed text
    :type doc: Spacy Doc
    :return: Verb Noun ratio
    :rtype: float
    """
    return pos_ratio(doc, 'VERB|AUX') / pos_ratio(doc, 'NOUN|PROPN')


def words_before_root(doc, max_depth=4):
    """Return average word count of words before root.

    For each sentence, word count before root is computed in the case that the
    root is a verb. Otherwise, the root is considered to be the verb in the
    highest node in the parse tree.

    :param doc: Text to be processed.
    :type doc: Spacy Doc
    :return: Average words before root
    :rtype: float
    """
    total_words_before_root = 0
    total_roots = 0
    for sent in doc.sents:
        root_is_verb = False
        verb_highest_node_found = False
        root = None
        for token in sent:
            if token.dep_ == "ROOT":
                root = token
                if token.pos_ in {"VERB", "AUX"}:
                    root_is_verb = True
        if not root_is_verb:
            for depth in range(2, max_depth):
                if not verb_highest_node_found:
                    for token in sent:
                        if token.pos_ in {"VERB", "AUX"}:
                            if get_word_depth(token.i, doc) == depth:
                                root = token
                                verb_highest_node_found = True
                                break

        root_found = False
        verb_root_found = root_is_verb or verb_highest_node_found
        words_before_root = 0
        for token in sent:
            if token == root and verb_root_found:
                root_found = True
                total_roots += 1
                total_words_before_root += words_before_root
            else:
                aux = token.pos_ != "PUNCT" and verb_root_found
                if (not root_found) and aux:
                    words_before_root += 1
    return total_words_before_root / total_roots


def word_count(doc):
    """Return number of words in a text.

    :param doc: Text to be processed.
    :type doc: Spacy Doc
    :return: Word count
    :rtype: int
    """
    return sum([1 for token in doc if is_word(token.pos_)])
