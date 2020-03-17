"""Unit tests for semantic measurements TRUNAJOD module."""
import mock
from TRUNAJOD import semantic_measures


def test_getSynsets():
    """Test get syn sets method."""
    synset = {
        'dummy1': {'dummy2', 'dummy3'},
    }
    assert semantic_measures.getSynsets('dummy1', synset) \
        == {'dummy2', 'dummy3'}

    assert semantic_measures.getSynsets('placeholder', synset) \
        == {'placeholder'}


def test_overlap():
    """Test get overlap method."""
    synset = {
        'dummy1': {'dummy2', 'dummy3'},
        'dummyx': {'dummy1'},
    }
    sentences = [
        ['dummy1', 'dummy4'],
        ['dummyx'],
    ]
    assert semantic_measures.overlap(sentences, synset) == 1.0


def test_avgW2VSemanticSimilarity():
    """Test word2vec semantic similarity method."""
    doc = mock.MagicMock()
    doc.similarity = mock.MagicMock(return_value=1)
    docs = mock.MagicMock()
    docs.__next__ = mock.MagicMock(side_effect=[doc, doc])
    assert semantic_measures.avgW2VSemanticSimilarity(docs, 2) == 1
