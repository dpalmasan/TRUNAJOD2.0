"""TRUNAJOD lexico semantic norms module.

Lexico-Semantic norms do also require external knowledge to be computed. We compute
the following lexico-semantic variables:

* Arousal
* Concreteness
* Context Availability
* Familiarity
* Imageability
* Valence

We provide two downloadable models of these variables, which come from
:cite:`duchon2013espal` and :cite:`guasch2016spanish`.
"""
from TRUNAJOD.lexicosemantic_norms_espal import LEXICOSEMANTIC_ESPAL
from TRUNAJOD.lexicosemantic_norms_espal import LSNorm
from TRUNAJOD.utils import lemmatize


class LexicoSemanticNorm(object):
    """Create a lexico semantic norm calculator for text.

    This requires a lexico semantic norm dict, with key-value pairs specified
    as ``word -> {"arousal", "concreteness", "context_availability",
    "familiarity", "imageability", "valence"}``. Average over number of
    tokens will be computed. The values are obtained from
    :cite:`guasch2016spanish`.
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


def get_conc_imag_familiarity(doc):
    """Get lexico-semantic variables.

    Computes three lexico-semantic variables: Concreteness, Imageability and
    Familiarity. The values are obtained from the EsPal dictionary (Spanish)
    and average of each metric is computed over sentences. To get each metric,
    the best practice is using `LSNorm Enum` defined in
    `lexicosemantic_norms_espal` module. The enums are `CONCRETENESS`,
    `IMAGEABILITY` and `FAMILIARITY`. This implementation uses values of the
    lexico-semantic norms from :cite:`duchon2013espal`.

    :param doc: Tokenized text
    :type doc: Spacy Doc
    :return: Concreteness imageability and familiarity averaged over sentences
    :rtype: List of float
    """
    n_found_tokens = [0, 0, 0]
    lsnorm_total = [0, 0, 0]

    for token in doc:
        if (token.pos_ == "NOUN"):
            lemma = token.lemma_
            if lemma in LEXICOSEMANTIC_ESPAL:
                concreteness, imageability, familiarity =\
                    LEXICOSEMANTIC_ESPAL[lemma.lower()]
                n_found_tokens = [x + 1 for x in n_found_tokens]
                lsnorm_total[LSNorm.CONCRETENESS] += concreteness
                lsnorm_total[LSNorm.IMAGEABILITY] += imageability
                lsnorm_total[LSNorm.FAMILIARITY] += familiarity

    lsnorm_total[LSNorm.CONCRETENESS] /= n_found_tokens[LSNorm.CONCRETENESS]
    lsnorm_total[LSNorm.IMAGEABILITY] /= n_found_tokens[LSNorm.IMAGEABILITY]
    lsnorm_total[LSNorm.FAMILIARITY] /= n_found_tokens[LSNorm.FAMILIARITY]
    return lsnorm_total
