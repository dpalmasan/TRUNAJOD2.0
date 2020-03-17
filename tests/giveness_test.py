"""Unit tests for giveness TRUNAJOD module."""
from collections import namedtuple

import mock
from TRUNAJOD import giveness

Token = namedtuple('Token', 'pos_ tag_')


def test_pronounDensity():
    """Test pronoun density method."""
    doc = mock.MagicMock()
    doc.__iter__.return_value = [
        Token('PRON', [giveness.THIRD_PERSON_LABEL]),
        Token('VERB', [])
    ]
    assert giveness.pronounDensity(doc) == 0.5


def test_pronounNounRatio():
    """Test pronoun noun ratio method."""
    doc = mock.MagicMock()
    doc.__iter__.return_value = [
        Token('PRON', [giveness.THIRD_PERSON_LABEL]),
        Token('NOUN', [])
    ]
    assert giveness.pronounNounRatio(doc) == 1.0
