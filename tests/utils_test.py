"""Unit tests for utils TRUNAJOD module."""
from typing import NamedTuple

import mock
from TRUNAJOD import utils


class Token(NamedTuple):
    """Implement Token mock for spacy.tokens.Token."""

    pos_: str


def test_is_stopword():
    """Test is stopword method."""
    stopwords = ["el", "la"]
    assert utils.is_stopword("la", stopwords)
    assert not utils.is_stopword("perro", stopwords)


def test_flatten():
    """Test is list flatten method."""
    result = utils.flatten([["hello"], ["world", "!"]])
    assert result[0] == "hello" and result[1] == "world" and result[2] == "!"


def test_lemmatize():
    """Test lemmatization method."""
    assert utils.lemmatize({"corriendo": "correr"}, "corriendo") == "correr"


def test_pos_booleans():
    """Test POS boolean methods."""
    assert utils.is_adjective(Token(pos_="ADJ"))
    assert utils.is_adverb(Token(pos_="ADV"))
    assert utils.is_noun(Token(pos_="NOUN"))
    assert utils.is_noun(Token(pos_="PROPN"))
    assert utils.is_pronoun(Token(pos_="PRON"))
    assert utils.is_verb(Token(pos_="VERB"))
    assert utils.is_word(Token(pos_="NOUN"))


@mock.patch("builtins.open", mock.mock_open(read_data="the"))
def test_get_stopwords():
    """Test get stopwords method."""
    result = utils.get_stopwords("stopwords")
    assert result == {"the"}
    open.assert_called_with("stopwords", "r", encoding="utf8")


@mock.patch("builtins.open", mock.mock_open(read_data="the"))
def test_read_text():
    """Test read text method."""
    result = utils.read_text("stopwords")
    assert result == "the"
    open.assert_called_with("stopwords", "r", encoding="utf8")
