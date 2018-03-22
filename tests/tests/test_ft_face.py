import os

import freetype


def test_ft_face():
    """A smoke test."""
    assert freetype.Face('../examples/Vera.ttf')

    if os.environ.get("FREETYPEPY_BUNDLE_FT"):
        assert freetype.version() == (2, 9, 0)
