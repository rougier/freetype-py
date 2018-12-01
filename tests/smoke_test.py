import glob
import os

import freetype
import pytest


def test_load_ft_face():
    """A smoke test."""
    assert freetype.Face('../examples/Vera.ttf')


def test_load_from_memfile():
    """Test loading from memory file"""
    with open('../examples/Vera.ttf') as f:
        assert freetype.Face(f)


def test_bundle_version():
    module_dir = os.path.dirname(freetype.__file__)
    shared_object = glob.glob(os.path.join(module_dir, "libfreetype*"))
    if shared_object:
        import re
        with open("../setup-build-freetype.py") as f:
            m = re.findall(r"freetype-(\d+)\.(\d+)\.?(\d+)?\.tar", f.read())
        version = m[0]
        if not version[2]:
            version = (int(version[0]), int(version[1]), 0)
        else:
            version = (int(version[0]), int(version[1]), int(version[2]))
        assert freetype.version() == version
    else:
        pytest.skip("Not using a bundled FreeType library.")
