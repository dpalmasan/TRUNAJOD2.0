"""TRUNAJOD emotions module.

These measurements are based on the lexicon from :cite:`rangel2014creacion`.
TRUNAJOD already comes bundled with this lexicon, in the following module
constant ``TRUNAJOD.spanish_emotion_lexicon.SPANISH_EMOTION_LEXICON``.

.. caution:: Keep in mind
   this module is still under development. Moreover
   only Spanish language is supported by this module as we are directly
   feeding the class with the lexicon.

The following emotions are captured: alegría, enojo, miedo, repulsión,
sorpresa, tristeza.
"""
from TRUNAJOD.spanish_emotion_lexicon import SPANISH_EMOTION_LEXICON
from TRUNAJOD.utils import lemmatize


class Emotions(object):
    """Compute emotions from SPANISH EMOTION LEXICON :cite:`rangel2014creacion`.

    Computes emotions based on Probability Factor of Affective use (PFA) and
    averaging over the total analized words from the text (that are found
    in the lexicon).

    Ideas:

    - How about not using PFA?
    - Averaging over emotions and not the total count?
    """

    def __init__(self, doc, lemmatizer=None):
        """Initialize emotions class.

        Average over number of tokens.

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
        """Get alegria.

        :return: Average alegria over number of tokens
        :rtype: float
        """
        return self.__alegria

    def get_enojo(self):
        """Get enojo.

        :return: Average enojo over number of tokens
        :rtype: float
        """
        return self.__enojo

    def get_miedo(self):
        """Get miedo.

        :return: Average miedo over number of tokens
        :rtype: float
        """
        return self.__miedo

    def get_repulsion(self):
        """Get repulsion.

        :return: Average repulsion over number of tokens
        :rtype: float
        """
        return self.__repulsion

    def get_sorpresa(self):
        """Get sorpresa.

        :return: Average sorpresa over number of tokens
        :rtype: float
        """
        return self.__sorpresa

    def get_tristeza(self):
        """Get tristeza.

        :return: Average tristeza over number of tokens
        :rtype: float
        """
        return self.__tristeza
