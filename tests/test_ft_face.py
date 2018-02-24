import freetype


def test_ft_face():
    """A smoke test."""
    assert freetype.Face('examples/Vera.ttf')