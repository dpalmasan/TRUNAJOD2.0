"""Unit tests for surface_proxies module."""
from collections import namedtuple

from TRUNAJOD import surface_proxies

Token = namedtuple("Token", ["word", "pos_", "lower_", "lemma_", "tag_"])
doc = [
    Token("El", "", "el", "El", "Person=1"),
    Token("perro", "NOUN", "perro", "perro", "tag"),
    Token("es", "", "es", "es", "tag"),
    Token("extraordinario", "ADJ", "extraordinario", "extraordinario", "tag"),
    Token(".", "PUNCT", ".", ".", "tag"),
]


def test_syllable_word_ratio():
    """Test syllable_word_count_ratio method."""
    assert surface_proxies.syllable_word_ratio(doc) == 10 / 4.0


def test_average_word_length():
    """Test average_word_length method."""
    assert surface_proxies.average_word_length(doc) == 23 / 4.0


def test_connection_words_ratio():
    """Test connection_words_ratio."""
    assert surface_proxies.connection_words_ratio(doc) == 0


def test_negation_density():
    """Test negation_density."""
    assert surface_proxies.negation_density(doc) == 0


def test_noun_count():
    """Test noun_count."""
    assert surface_proxies.noun_count(doc) == 1


def test_first_second_person_density():
    """Test first_second_person_density."""
    assert surface_proxies.first_second_person_count(doc) == 1


def test_infinitive():
    """Test infinitive."""
    assert surface_proxies.infinitve("comiendo", {}) is None
    assert (
        surface_proxies.infinitve("comiendo", {"comiendo": "comer"}) == "comer"
    )
