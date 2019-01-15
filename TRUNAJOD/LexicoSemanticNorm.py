#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from .utils import lemmatize


class LexicoSemanticNorm(object):
    def __init__(self, doc, lexico_semantic_norm_dict, lemmatizer=None):

        valence = 0
        arousal = 0
        concreteness = 0
        imageability = 0
        context_availability = 0
        familiarity = 0
        count = 0.0

        for token in doc:
            word = token.text.lower()
            word_lemma = word
            if lemmatizer:
                word_lemma = lemmatize(lemmatizer, word)

            if word in lexico_semantic_norm_dict:
                valence += lexico_semantic_norm_dict[word].get("valence")
                arousal += lexico_semantic_norm_dict[word].get("arousal")
                concreteness += (
                    lexico_semantic_norm_dict[word].get("concreteness")
                )
                imageability += (
                    lexico_semantic_norm_dict[word].get("imageability")
                )
                context_availability += (
                    lexico_semantic_norm_dict[word].get("context_availability")
                )
                familiarity += (
                    lexico_semantic_norm_dict[word].get("familiarity")
                )
                count += 1
            elif word_lemma in lexico_semantic_norm_dict:
                word = word_lemma
                valence += lexico_semantic_norm_dict[word].get("valence")
                arousal += lexico_semantic_norm_dict[word].get("arousal")
                concreteness += (
                    lexico_semantic_norm_dict[word].get("concreteness")
                )
                imageability += (
                    lexico_semantic_norm_dict[word].get("imageability")
                )
                context_availability += (
                    lexico_semantic_norm_dict[word].get("context_availability")
                )
                familiarity += (
                    lexico_semantic_norm_dict[word].get("familiarity")
                )
                count += 1.0

        self.__valence = valence
        self.__arousal = arousal
        self.__concreteness = concreteness
        self.__imageability = imageability
        self.__context_avilability = context_availability
        self.__familiarity = familiarity
        if count > 0:
            self.__valence /= count
            self.__arousal /= count
            self.__concreteness /= count
            self.__imageability /= count
            self.__context_avilability /= count
            self.__familiarity /= count

    def get_valence(self):
        return self.__valence

    def get_arousal(self):
        return self.__arousal

    def get_concreteness(self):
        return self.__concreteness

    def get_imageability(self):
        return self.__imageability

    def get_context_availability(self):
        return self.__context_avilability

    def get_familiarity(self):
        return self.__familiarity
