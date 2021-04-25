"""Define model for languages."""
from typing import Any
from typing import Dict


class Language:
    """Class that hold data for a specific language.

    For example, given that Spanish model was installed, this
    class holds infinitve map, frequency indices, and any
    resource defined in the model.
    """

    def __init__(self, *, meta: Dict[str, Any] = {}):
        """Initialize a Language object.

        :param meta: model's metadata, defaults to {}
        :type meta: Dict[str, Any], optional
        """
        self.lang = None
        self._meta = dict(meta)

    @property
    def meta(self) -> Dict[str, Any]:
        """Metadata of the language class.

        If a model is loaded, this includes details from the
        model's meta.json
        """
        self._meta.setdefault("lang", self.lang)
        self._meta.setdefault("version", "0.0.0")
        self._meta.setdefault("description", "")
        self._meta.setdefault("author", "")
        self._meta.setdefault("email", "")
        self._meta.setdefault("url", "")
        self._meta.setdefault("license", "")
        return self._meta

    @meta.setter
    def meta(self, value: Dict[str, Any]) -> None:
        """Metadata setter."""
        self._meta = value
