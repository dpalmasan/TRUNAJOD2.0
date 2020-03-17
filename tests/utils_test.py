from TRUNAJOD import utils


def test_isStopword():
    stopwords = ['el', 'la']
    assert utils.isStopword('la', stopwords)
    assert not utils.isStopword('perro', stopwords)


def test_flatten():
    result = utils.flatten([['hello'], ['world', '!']])
    assert result[0] == 'hello' \
        and result[1] == 'world' \
        and result[2] == '!'


def test_lemmatize():
    assert utils.lemmatize({'corriendo': 'correr'}, 'corriendo') \
        == 'correr'
