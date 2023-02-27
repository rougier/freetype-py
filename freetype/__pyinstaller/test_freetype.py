def test_pyi_freetype(pyi_builder):
    pyi_builder.test_source(
        """
        import freetype
        """
    )
