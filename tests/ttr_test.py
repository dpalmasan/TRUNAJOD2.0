"""TRUNAJOD ttr tests."""
from collections import namedtuple

from TRUNAJOD import ttr


def test_type_token_ratio():
    """Test type_token_ratio func."""
    assert ttr.type_token_ratio(
        ['hola', 'hola', 'chao', 'hola', 'perro', 'hola'], ) == 0.5


def test_one_side_lexical_diversity_mtld():
    """Test one_side_lexical_diversity_mtld."""
    assert ttr.one_side_lexical_diversity_mtld(
        ['hola', 'hola', 'chao', 'hola', 'perro', 'hola'], 1) == 3


def test_lexical_diversity_mtld():
    """Test lexical_diversity_mtld."""
    Token = namedtuple("Token", "lemma_ pos_")
    doc = [
        Token('hola', 'hola'),
        Token('hola', 'hola'),
        Token('chao', 'chao'),
        Token('hola', 'hola'),
        Token('perro', 'perro'),
        Token('hola', 'hola'),
    ]
    assert ttr.lexical_diversity_mtld(doc, 1) == 3
