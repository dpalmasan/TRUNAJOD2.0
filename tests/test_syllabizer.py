"""Unit tests for silabizator module."""
from TRUNAJOD.syllabizer import CharLine
from TRUNAJOD.syllabizer import Syllabizer


def test_char_line():
    """Test CharLine class."""
    assert CharLine.char_type("a") == "V"
    assert CharLine.char_type("i") == "v"
    assert CharLine.char_type("x") == "x"
    assert CharLine.char_type("s") == "s"
    assert CharLine.char_type("z") == "c"

    charline = CharLine("extraordinario")
    assert str(charline) == "<extraordinario:VxccVVccvcVcvV>"
    assert charline.find("cc") == 2
    c1, c2 = charline.split(0, 5)
    assert str(c1) == "<extra:VxccV>"
    assert str(c2) == "<ordinario:VccvcVcvV>"


def test_syllabizer():
    """Test silabizer class."""
    r1, r2 = Syllabizer.split(CharLine("veinte"))
    assert r1 == CharLine("vein")
    assert r2 == CharLine("te")

    assert Syllabizer.number_of_syllables("increíble") == 4
    assert Syllabizer.number_of_syllables("águila") == 3
