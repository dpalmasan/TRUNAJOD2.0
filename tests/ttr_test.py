"""TRUNAJOD ttr tests."""
from collections import namedtuple

from TRUNAJOD import ttr


def test_type_token_ratio():
    """Test type_token_ratio func."""
    assert (
        ttr.type_token_ratio(["hola", "hola", "chao", "hola", "perro", "hola"])
        == 0.5
    )


def test_one_side_lexical_diversity_mtld():
    """Test one_side_lexical_diversity_mtld."""
    assert (
        ttr.one_side_lexical_diversity_mtld(
            ["hola", "hola", "chao", "hola", "perro", "hola"], ttr_segment=1
        )
        == 3
    )


def test_lexical_diversity_mtld():
    """Test lexical_diversity_mtld."""
    Token = namedtuple("Token", "lemma_ pos_")
    doc = [
        Token("hola", "hola"),
        Token("hola", "hola"),
        Token("chao", "chao"),
        Token("hola", "hola"),
        Token("perro", "perro"),
        Token("hola", "hola"),
    ]
    assert ttr.lexical_diversity_mtld(doc, ttr_segment=1) == 3


def test_yule_k():
    """Test yule_k."""
    Token = namedtuple("Token", "lemma_ pos_")
    doc = [
        Token("hola", "hola"),
        Token("hola", "hola"),
        Token("chao", "chao"),
        Token("hola", "hola"),
        Token("perro", "perro"),
        Token("hola", "hola"),
    ]

    n = len(doc)
    rs = {
        1: 2,
        4: 1,
    }
    expected_k = 1e-4 * sum(r ** 2 * vr - n for r, vr in rs.items()) / n ** 2
    assert ttr.yule_k(doc) == expected_k
