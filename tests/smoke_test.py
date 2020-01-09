import glob
import os

import freetype
import pytest

test_folder = os.path.realpath(os.path.dirname(__file__))


def test_load_ft_face():
    """A smoke test."""
    p = os.path.join(test_folder, "..", "examples", "Vera.ttf")
    assert freetype.Face(p)


def test_load_ft_face_from_memory():
    """Another smoke test."""
    p = os.path.join(test_folder, "..", "examples", "Vera.ttf")
    with open(p, mode="rb") as f:
        assert freetype.Face(f)

    with open(p, mode="rb") as f:
        byte_stream = f.read()
    assert freetype.Face.from_bytes(byte_stream)


def test_bundle_version():
    module_dir = os.path.dirname(freetype.__file__)
    shared_object = glob.glob(os.path.join(module_dir, "libfreetype*"))
    if shared_object:
        import re
        p = os.path.join(test_folder, "..", "setup-build-freetype.py")
        with open(p) as f:
            m = re.findall(r"freetype-(\d+)\.(\d+)\.?(\d+)?\.tar", f.read())
        version = m[0]
        if not version[2]:
            version = (int(version[0]), int(version[1]), 0)
        else:
            version = (int(version[0]), int(version[1]), int(version[2]))
        assert freetype.version() == version
    else:
        pytest.skip("Not using a bundled FreeType library.")
