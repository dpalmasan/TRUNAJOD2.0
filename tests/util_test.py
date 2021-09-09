"""Unit tests for Language loading utilities."""
import json
from pathlib import Path

from TRUNAJOD import _util


def test_load_meta(tmpdir):
    """Test load_meta."""
    fp = tmpdir.mkdir("test_data").join("meta.json")
    fp.write(
        json.dumps(
            {
                "lang": "es",
                "name": "trunajod",
                "version": "v0.0.0",
                "env": "pytest",
            }
        )
    )
    path = Path(fp.strpath)
    assert _util.load_meta(path) == {
        "lang": "es",
        "name": "trunajod",
        "version": "v0.0.0",
        "env": "pytest",
    }
