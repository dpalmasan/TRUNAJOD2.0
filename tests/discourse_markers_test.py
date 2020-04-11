"""Unit tests for discourse_markers TRUNAJOD module."""
from collections import namedtuple

from TRUNAJOD import discourse_markers

# Use this to avoid spacy Doc dependency on testing
Doc = namedtuple("Doc", "sents")
Text = namedtuple("Text", "string")


def test_find_matches():
    """Test find_matches method."""
    result = discourse_markers.find_matches(
        "Hola mundo ola mundo! hay una ola.", ["ola", "hay"])
    assert result == 3


def test_get_cause_dm_count():
    """Test get_cause_dm_count method."""
    result = discourse_markers.get_cause_dm_count(
        Doc([
            Text("En realidad la pandemia no es mala."),
            Text("Porque no es mortal.")
        ]))
    assert result == 0.5


def test_get_closed_class_vague_meaning_count():
    """Test get_closed_class_vague_meaning_count method."""
    result = discourse_markers.get_closed_class_vague_meaning_count(
        Doc([
            Text("En realidad la pandemia no es mala."),
            Text("En contra de lo que se cree no es tan mortal.")
        ]))
    assert result == 2


def test_get_context_dm_count():
    """Test get_context_dm_count method."""
    result = discourse_markers.get_context_dm_count(
        Doc([
            Text("Teniendo en cuenta las medidas de prevención."),
            Text("Se evitarán muchas muertes.")
        ]))
    assert result == 0.5


def test_get_revision_dm_count():
    """Test get_revision_dm_count method."""
    result = discourse_markers.get_revision_dm_count(
        Doc([
            Text("En realidad la pandemia no es mala."),
            Text("No obstante hay que cuidarse.")
        ]))
    assert result == 1
