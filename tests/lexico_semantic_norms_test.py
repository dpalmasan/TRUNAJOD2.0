"""Unit tests for emotions TRUNAJOD module."""
from collections import namedtuple

from TRUNAJOD.lexico_semantic_norms import LexicoSemanticNorm

# Use this to avoid spacy Doc dependency on testing
Token = namedtuple("Token", "text")


def _init_lexical_dict(value):
    return {
        "valence": value,
        "arousal": value,
        "concreteness": value,
        "imageability": value,
        "context_availability": value,
        "familiarity": value
    }


def test_lexico_semantic_norm():
    """Test LexicoSemanticNorm class."""
    lemmatizer = {
        "abundanciaa": "abundancia",
        "abominacióna": "abominación",
        "atroza": "atroz",
        "cocolíaa": "cocolía",
        "admirablea": "admirable",
        "almaa": "alma"
    }

    lexico_semantic_norms = {
        "abundancia": _init_lexical_dict(1),
        "abominación": _init_lexical_dict(2),
        "atroz": _init_lexical_dict(3),
        "cocolía": _init_lexical_dict(4),
        "admirable": _init_lexical_dict(5),
        "alma": _init_lexical_dict(6),
    }

    lexico_semantic_norms_calc = LexicoSemanticNorm([
        Token("Abundancia"),
        Token("abominación"),
        Token("atroz"),
        Token("cocolía"),
        Token("admirable"),
        Token("alma")
    ], lexico_semantic_norms)

    assert lexico_semantic_norms_calc.get_arousal() == 21 / 6.0
    assert lexico_semantic_norms_calc.get_concreteness() == 21 / 6.0
    assert lexico_semantic_norms_calc.get_context_availability() == 21 / 6.0
    assert lexico_semantic_norms_calc.get_familiarity() == 21 / 6.0
    assert lexico_semantic_norms_calc.get_imageability() == 21 / 6.0
    assert lexico_semantic_norms_calc.get_valence() == 21 / 6.0

    lexico_semantic_norms_calc = LexicoSemanticNorm([
        Token("Abundanciaa"),
        Token("abominacióna"),
        Token("atroza"),
        Token("cocolíaa"),
        Token("admirablea"),
        Token("almaa")
    ], lexico_semantic_norms, lemmatizer)

    assert lexico_semantic_norms_calc.get_arousal() == 21 / 6.0
    assert lexico_semantic_norms_calc.get_concreteness() == 21 / 6.0
    assert lexico_semantic_norms_calc.get_context_availability() == 21 / 6.0
    assert lexico_semantic_norms_calc.get_familiarity() == 21 / 6.0
    assert lexico_semantic_norms_calc.get_imageability() == 21 / 6.0
    assert lexico_semantic_norms_calc.get_valence() == 21 / 6.0
