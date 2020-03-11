from TRUNAJOD import ttr


def test_isStopword():
    assert ttr.simple_ttr([]) == 0
    assert ttr.simple_ttr(
        ['hola', 'hola', 'chao', 'hola', 'perro', 'hola'],
    ) == 0.5
