"""TRUNAJOD lexico semantic norms module."""
from TRUNAJOD.utils import lemmatize


class LexicoSemanticNorm(object):
    """Create a lexico semantic norm calculator for text.

    This requires a lexico semantic norm dict, with key-value pairs specified
    as word -> {"arousal", "concreteness", "context_availability",
    "familiarity", "imageability", "valence"}. Average over number of
    tokens will be computed.
    """

    def __init__(self, doc, lexico_semantic_norm_dict, lemmatizer=None):
        """Initialize lexico semantic norm object.

        Calculate average over number of tokens given a text.

        :param doc: Text to be processed
        :type doc: Spacy Doc
        :param lexico_semantic_norm_dict: Lexico semantic norms for words
        :type lexico_semantic_norm_dict: dict
        :param lemmatizer: Lemmatizer, defaults to None
        :type lemmatizer: dict, optional
        """
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
                    lexico_semantic_norm_dict[word].get("concreteness"))
                imageability += (
                    lexico_semantic_norm_dict[word].get("imageability"))
                context_availability += (lexico_semantic_norm_dict[word].get(
                    "context_availability"))
                familiarity += (
                    lexico_semantic_norm_dict[word].get("familiarity"))
                count += 1
            elif word_lemma in lexico_semantic_norm_dict:
                word = word_lemma
                valence += lexico_semantic_norm_dict[word].get("valence")
                arousal += lexico_semantic_norm_dict[word].get("arousal")
                concreteness += (
                    lexico_semantic_norm_dict[word].get("concreteness"))
                imageability += (
                    lexico_semantic_norm_dict[word].get("imageability"))
                context_availability += (lexico_semantic_norm_dict[word].get(
                    "context_availability"))
                familiarity += (
                    lexico_semantic_norm_dict[word].get("familiarity"))
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

    def get_arousal(self):
        """Get arousal.

        :return: Average arousal.
        :rtype: float
        """
        return self.__arousal

    def get_concreteness(self):
        """Get concreteness.

        :return: Average concreteness.
        :rtype: float
        """
        return self.__concreteness

    def get_context_availability(self):
        """Get context_availability.

        :return: Average context_availability.
        :rtype: float
        """
        return self.__context_avilability

    def get_familiarity(self):
        """Get familiarity.

        :return: Average familiarity.
        :rtype: float
        """
        return self.__familiarity

    def get_imageability(self):
        """Get imageability.

        :return: Average imageability.
        :rtype: float
        """
        return self.__imageability

    def get_valence(self):
        """Get valence.

        :return: Average valence.
        :rtype: float
        """
        return self.__valence
