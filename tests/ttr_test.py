"""TRUNAJOD ttr tests."""
import string
from collections import namedtuple

import numpy as np
import pytest
from TRUNAJOD import ttr


Token = namedtuple("Token", ["lemma_", "pos_"])


@pytest.fixture
def test_doc():
    """Fixture to use a doc for tests."""
    doc = [
        Token(lemma_="hola", pos_="hola"),
        Token(lemma_="hola", pos_="hola"),
        Token(lemma_="chao", pos_="chao"),
        Token(lemma_="hola", pos_="hola"),
        Token(lemma_="perro", pos_="perro"),
        Token(lemma_="hola", pos_="hola"),
    ]
    yield doc


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


def test_lexical_diversity_mtld(test_doc):
    """Test lexical_diversity_mtld."""
    assert ttr.lexical_diversity_mtld(test_doc, ttr_segment=1) == 3


def test_yule_k(test_doc):
    """Test yule_k."""
    n = len(test_doc)
    rs = {
        1: 2,
        4: 1,
    }
    expected_k = 1e4 * sum(r ** 2 * vr - n for r, vr in rs.items()) / n ** 2
    assert ttr.yule_k(test_doc) == expected_k


def test_d_estimate():
    """Test d_estimate."""
    text = (
        "El espermatozoide y el ovocito son células son muy diferentes entre "
        "sí, y poseen propiedades estructurales que van adquiriendo mediante "
        "el proceso de gametogénesis. La gametogénesis masculina se denomina "
        "espermatogénesis y la femenina, ovogénesis. Ocurre al interior de "
        "los testículos, en unas estructuras llamadas túbulos seminíferos Se "
        "inicia en la pubertad y, en condiciones normales, se mantiene "
        "durante toda la vida de los hombres. A continuación, revisaremos sus "
        "etapas. Durante el desarrollo embrionario, las células germinales "
        "primordiales se multiplican, dando lugar a espermatogonias. Años más "
        "tarde, en la pubertad, algunas espermatogonias proliferan, aumentan "
        "de tamaño y se diferencian en espermatocitos primarios o "
        "espermatocitos I. Luego, los espermatocitos I pasan por un proceso "
        "que consta de dos divisiones celulares. La primera división, origina "
        "los espermatocitos secundarios o espermatocitos II; estas células "
        "experimentan la segunda división formando las espermátidas. Cada una "
        "de ellas tiene la mitad del material genético de la especie. "
        "Finalmente, las espermátidas experimentan cambios morfológicos que "
        "darán origen a los espermatozoides."
    )

    doc = []
    for token in text.translate(
        str.maketrans("", "", string.punctuation)
    ).split():
        word_lower = token.lower()
        doc.append(Token(lemma_=token, pos_=token))

    np.random.seed(0)
    assert ttr.d_estimate(doc) == 119.4468681409897


def test_hapax_legomena_index():
    """Test hapax_legomena_index."""
    Token = namedtuple("Token", "lemma_ pos_")
    doc = [
        Token("hola", "hola"),
        Token("hola", "hola"),
        Token("chao", "chao"),
        Token("hola", "hola"),
        Token("perro", "perro"),
        Token("hola", "hola"),
    ]

    answer = 2
    assert ttr.hapax_legomena_index(doc) == answer
