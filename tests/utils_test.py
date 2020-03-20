"""Unit tests for utils TRUNAJOD module."""
import mock
from TRUNAJOD import utils


def test_isStopword():
    """Test is stopword method."""
    stopwords = ['el', 'la']
    assert utils.isStopword('la', stopwords)
    assert not utils.isStopword('perro', stopwords)


def test_flatten():
    """Test is list flatten method."""
    result = utils.flatten([['hello'], ['world', '!']])
    assert result[0] == 'hello' \
        and result[1] == 'world' \
        and result[2] == '!'


def test_lemmatize():
    """Test lemmatization method."""
    assert utils.lemmatize({'corriendo': 'correr'}, 'corriendo') \
        == 'correr'


def test_pos_booleans():
    """Test POS boolean methods."""
    assert utils.isAdjective("ADJ")
    assert utils.isAdverb("ADV")
    assert utils.isNoun("NOUN")
    assert utils.isNoun("PROPN")
    assert utils.isPronoun("PRON")
    assert utils.isVerb("VERB")
    assert utils.isWord("NOUN")


@mock.patch("builtins.open", mock.mock_open(read_data='the'))
def test_getStopwords():
    """Test get stopwords method."""
    result = utils.getStopwords("stopwords")
    assert result == {'the'}
    open.assert_called_with('stopwords', 'r', 'utf8')


@mock.patch("builtins.open", mock.mock_open(read_data='the'))
def test_readText():
    """Test read text method."""
    result = utils.readText("stopwords")
    assert result == 'the'
    open.assert_called_with('stopwords', 'r', 'utf8')
