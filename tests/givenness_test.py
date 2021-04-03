"""Unit tests for giveness TRUNAJOD module."""
from collections import namedtuple

import mock
from TRUNAJOD import givenness

Token = namedtuple("Token", "pos_ tag_")


def test_pronoun_density():
    """Test pronoun density method."""
    doc = mock.MagicMock()
    doc.__iter__.return_value = [
        Token("PRON", [givenness.THIRD_PERSON_LABEL]),
        Token("VERB", []),
    ]
    assert givenness.pronoun_density(doc) == 0.5


def test_pronoun_noun_ratio():
    """Test pronoun noun ratio method."""
    doc = mock.MagicMock()
    doc.__iter__.return_value = [
        Token("PRON", [givenness.THIRD_PERSON_LABEL]),
        Token("NOUN", []),
    ]
    assert givenness.pronoun_noun_ratio(doc) == 1.0
