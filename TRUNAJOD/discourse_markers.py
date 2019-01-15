#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


CAUSE_DISCOURSE_MARKERS = set([
    u"dado que",
    u"porque",
    u"debido a",
    u"gracias a",
    u"por si",
    u"por",
    u"por eso",
    u"en conclusión",
    u"así que",
    u"como consecuencia",
    u"para",
    u"para que",
    u"por esta razón",
    u"por tanto",
    u"en efecto",
])

REVISION_DISCOURSE_MARKERS = set([
    u"a pesar de",
    u"aunque",
    u"excepto",
    u"pese a",
    u"no obstante",
    u"sin embargo",
    u"en realidad",
    u"de hecho",
    u"al contrario",
    u"el hecho es que",
    u"es cierto que",
    u"pero",
    u"con todo",
    u"ahora bien",
    u"de todos modos",
])

EQUALITY_DISCOURSE_MARKERS = set([
    u"en resumen",
    u"concretamente",
    u"en esencia",
    u"en comparación",
    u"en otras palabras",
    u"en particular",
    u"es decir",
    u"por ejemplo",
    u"precisamente",
    u"tal como",
    u"por último",
    u"por un lado",
    u"por otro lado",
    u"a propósito",
    u"no sólo",
    u"sino también",
    u"en dos palabras",
    u"además",
    u"también",
    u"aparte",
    u"aún es más",
    u"incluso",
    u"especialmente",
    u"sobretodo",
])

CAUSE_DISCOURSE_MARKERS = set([
    u"dado que",
    u"porque",
    u"debido a",
    u"gracias a",
    u"por si",
    u"por",
    u"por eso",
    u"en conclusión",
    u"así que",
    u"como consecuencia",
    u"para",
    u"para que",
    u"por esta razón",
    u"por tanto",
    u"en efecto",
])

CONTEXT_DISCOURSE_MARKERS = set([
    u"teniendo en cuenta",
    u"después",
    u"antes",
    u"originalmente",
    u"a condición de",
    u"durante",
    u"mientras",
    u"a no ser que",
    u"cuando",
    u"donde",
    u"de acuerdo con",
    u"lejos de",
    u"tan pronto como",
    u"por el momento",
    u"entre",
    u"hacia",
    u"hasta",
    u"mediante",
    u"según",
    u"en cualquier caso",
    u"entonces",
    u"respecto a",
    u"en ese caso",
    u"si",
    u"siempre que",
    u"sin duda",
    u"a la vez",
])

HIGHLY_POLYSEMIC_DISCOURSE_MARKERS = set([
    u"como",
    u"desde",
    u"sobre",
    u"antes que nada",
    u"para empezar",
])

VAGUE_MEANING_CLOSED_CLASS_WORDS = set([
    u"y",
    u"e",
    u"ni",
    u"o",
    u"u",
    u"que",
    u"con",
    u"sin",
    u"contra",
    u"en",
    u"a",
])


def find_matches(text, list):
    """
    Given a text and a list of possible matches (in this module, discourse
    markers list), returns the number of matches found in text.
    """
    counter = 0
    for w in list:
        results = re.findall(r"\b%s\b" % w, text, re.IGNORECASE)
        counter += len(results)
    return counter


def get_revision_dm_count(text):
    return find_matches(text, REVISION_DISCOURSE_MARKERS)


def get_cause_dm_count(text):
    return find_matches(text, CAUSE_DISCOURSE_MARKERS)


def get_equality_dm_count(text):
    return find_matches(text, EQUALITY_DISCOURSE_MARKERS)


def get_context_dm_count(text):
    return find_matches(text, CONTEXT_DISCOURSE_MARKERS)


def get_polysemic_dm_count(text):
    return find_matches(text, HIGHLY_POLYSEMIC_DISCOURSE_MARKERS)


def get_closed_class_vague_meaning_count(text):
    return find_matches(text, VAGUE_MEANING_CLOSED_CLASS_WORDS)
