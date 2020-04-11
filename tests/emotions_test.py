"""Unit tests for emotions TRUNAJOD module."""
from collections import namedtuple

from TRUNAJOD.emotions import Emotions
from TRUNAJOD.spanish_emotion_lexicon\
    import SPANISH_EMOTION_LEXICON

# Use this to avoid spacy Doc dependency on testing
Token = namedtuple("Token", "text")


def test_emotions():
    """Test Emotions class."""
    emotions = Emotions([
        Token("Abundancia"),
        Token("abominación"),
        Token("atroz"),
        Token("cocolía"),
        Token("admirable"),
        Token("alma")
    ])

    assert emotions.get_alegria() ==\
        SPANISH_EMOTION_LEXICON["abundancia"][0]/6

    assert emotions.get_enojo() ==\
        SPANISH_EMOTION_LEXICON["abominación"][0]/6

    assert emotions.get_miedo() ==\
        SPANISH_EMOTION_LEXICON["atroz"][0]/6

    assert emotions.get_repulsion() ==\
        SPANISH_EMOTION_LEXICON["cocolía"][0]/6

    assert emotions.get_sorpresa() ==\
        SPANISH_EMOTION_LEXICON["admirable"][0]/6

    assert emotions.get_tristeza() ==\
        SPANISH_EMOTION_LEXICON["alma"][0]/6

    emotions = Emotions(
        [
            Token("Abundanciaa"),
            Token("abominacióna"),
            Token("atroza"),
            Token("cocolíaa"),
            Token("admirablea"),
            Token("almaa")
        ], {
            "abundanciaa": "abundancia",
            "abominacióna": "abominación",
            "atroza": "atroz",
            "cocolíaa": "cocolía",
            "admirablea": "admirable",
            "almaa": "alma"
        })

    assert emotions.get_alegria() ==\
        SPANISH_EMOTION_LEXICON["abundancia"][0]/6

    assert emotions.get_enojo() ==\
        SPANISH_EMOTION_LEXICON["abominación"][0]/6

    assert emotions.get_miedo() ==\
        SPANISH_EMOTION_LEXICON["atroz"][0]/6

    assert emotions.get_repulsion() ==\
        SPANISH_EMOTION_LEXICON["cocolía"][0]/6

    assert emotions.get_sorpresa() ==\
        SPANISH_EMOTION_LEXICON["admirable"][0]/6

    assert emotions.get_tristeza() ==\
        SPANISH_EMOTION_LEXICON["alma"][0]/6
