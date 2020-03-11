#!/usr/local/bin/python
from .SpanishEmotionLexicon import SPANISH_EMOTION_LEXICON
from .utils import lemmatize


class Emotions:
    """Clase para definir emociones en español.

    Calcula emociones en base a PFA y promediando considerando todas las
    palabras que generan emociones (respecto al total de palabras analizadas).
    Ideas:
    - Probar sin PFA?
    - Ponderar PFA respecto a emociones y no del total?
    """

    def __init__(self, doc, lemmatizer=None):
        """Constructor de la instancia de emociones.

        :param doc: Texto a ser procesado
        :type doc: Spacy Doc
        :param lemmatizer: Lematizador a utilizar, defaults to None
        :type lemmatizer: Python dict, optional
        """
        alegria = 0
        enojo = 0
        miedo = 0
        repulsion = 0
        sorpresa = 0
        tristeza = 0
        count = 0.0

        for token in doc:
            word = token.text.lower()
            word_lemma = word
            if lemmatizer:
                word_lemma = lemmatize(lemmatizer, word)

            if word in SPANISH_EMOTION_LEXICON:
                pfa, emotion = SPANISH_EMOTION_LEXICON[word]
                if emotion == 'Alegría':
                    alegria += pfa
                elif emotion == 'Enojo':
                    enojo += pfa
                elif emotion == 'Miedo':
                    miedo += pfa
                elif emotion == 'Repulsión':
                    repulsion += pfa
                elif emotion == 'Sorpresa':
                    sorpresa += pfa
                else:
                    tristeza += pfa
                count += 1
            elif word_lemma in SPANISH_EMOTION_LEXICON:
                word = word_lemma
                pfa, emotion = SPANISH_EMOTION_LEXICON[word]
                if emotion == 'Alegría':
                    alegria += pfa
                elif emotion == 'Enojo':
                    enojo += pfa
                elif emotion == 'Miedo':
                    miedo += pfa
                elif emotion == 'Repulsión':
                    repulsion += pfa
                elif emotion == 'Sorpresa':
                    sorpresa += pfa
                else:
                    tristeza += pfa
                count += 1.0

        self.__alegria = alegria
        self.__enojo = enojo
        self.__miedo = miedo
        self.__repulsion = repulsion
        self.__sorpresa = sorpresa
        self.__tristeza = tristeza
        if count > 0:
            self.__alegria /= count
            self.__enojo /= count
            self.__miedo /= count
            self.__repulsion /= count
            self.__sorpresa /= count
            self.__tristeza /= count

    def get_alegria(self):
        return self.__alegria

    def get_enojo(self):
        return self.__enojo

    def get_miedo(self):
        return self.__miedo

    def get_repulsion(self):
        return self.__repulsion

    def get_sorpresa(self):
        return self.__sorpresa

    def get_tristeza(self):
        return self.__tristeza
