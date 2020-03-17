from TRUNAJOD import semantic_measures


def test_getSynsets():
    synset = {
        'dummy1': {'dummy2', 'dummy3'},
    }
    assert semantic_measures.getSynsets('dummy1', synset) \
        == {'dummy2', 'dummy3'}

    assert semantic_measures.getSynsets('placeholder', synset) \
        == {'placeholder'}


def test_overlap():
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
    assert semantic_measures.avgW2VSemanticSimilarity(
        [], 0,
    ) == 0.0
