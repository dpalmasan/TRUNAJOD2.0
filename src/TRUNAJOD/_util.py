"""Utilities used by model loader."""
from pathlib import Path
from typing import Any
from typing import Dict

import srsly

from .language import Language


METADATA_FILENAME = "meta.json"


def load_model(name: str) -> Language:
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

    meta = get_model_meta(model_path)


def get_model_meta(path: Path) -> Dict[str, Any]:
    """Get metadata from model.

    :param path: Path to load meta from
    :type path: Path
    :return: Metadata dict
    :rtype: Dict[str, Any]
    """
    return load_meta(path / METADATA_FILENAME)


def load_meta(path: Path) -> Dict[str, Any]:
    """Load and validate metadata file.

    :param path: Path of the metadata file
    :type path: Path
    :raises IOError: If E03, E04 happens (placeholder)
    :raises ValueError: If metadata is invalid
    :return: Metadata dict
    :rtype: Dict[str, Any]
    """
    if not path.parent.exists():
        raise IOError("Not exists!")

    if not path.exists() or not path.is_file():
        raise IOError("Cannot load json!")

    meta = srsly.read_json(path)
    for setting in ("lang", "name", "version"):
        if setting not in meta or not meta[setting]:
            raise ValueError("Required metadata not found!")

    return meta
