"""TRUNAJOD init module."""
from pathlib import Path
from typing import Union

from .language import Language


def load(name: Union[str, Path]) -> Language:
    """Load a TRUNAJOD model from a local path.

    :param name: Model name
    :type name: Union[str, Path]
    :return: A TRUNAJOD language model.
    :rtype: Language
    """
    return _util.load_model(name)
