"""Utilities used by model loader."""
from pathlib import Path
from typing import Union

from .language import Language


def load_model(name: Union[str, Path]) -> Language:
    """Load a TRUNAJOD model.

    :param name: [description]
    :type name: Union[str, Path]
    :return: [description]
    :rtype: Language
    """
    if isinstance(name, str):
        if Path(name).exists():
            return load_model_from_path(Path(name))


def load_model_from_path(model_path: Path) -> Language:
    """Load a model from path, provided it was installed."""
    if not model_path.exists():
        raise IOError("Model does not exist!")
