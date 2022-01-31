#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
'''
Basic outline wrapper test
'''
from freetype import *
import ctypes
import contextlib

@contextlib.contextmanager
def new_outline(n_points, n_contours):
    library = get_handle()
    raw_ft_outline = FT_Outline()
    err = FT_Outline_New(
        library, FT_UInt(n_points), FT_Int(n_contours),
        ctypes.byref(raw_ft_outline)
    )
    if err: raise FT_Exception(error)
    try:
        raw_ft_outline.n_points   = 0
        raw_ft_outline.n_contours = 0
        yield Outline(raw_ft_outline)
    finally:
        FT_Outline_Done(library, ctypes.byref(raw_ft_outline))

if __name__ == '__main__':
    face = Face('./Vera.ttf')
    face.set_char_size( 4*48*64 )
    flags = FT_LOAD_DEFAULT | FT_LOAD_NO_BITMAP
    face.load_char('S', flags )
    slot = face.glyph
    outline = slot.outline

    bbox = outline.get_bbox()
    cbox = outline.get_cbox()
    assert (bbox.xMin, bbox.yMin, bbox.xMax, bbox.yMax) == \
        (810, -192, 7116, 9152)
    assert (cbox.xMin, cbox.yMin, cbox.xMax, cbox.yMax) == \
        (810, -192, 7116, 9152)
    assert outline.get_outside_border() == 0
    assert outline.get_inside_border() == 1
    assert len(outline.contours) == 1
    assert len(outline.points) == 40
    assert len(outline.tags) == 40

    stroker = Stroker()
    stroker.set(64, FT_STROKER_LINECAP_ROUND, FT_STROKER_LINEJOIN_ROUND, 0)
    stroker.parse_outline(outline, False)

    n_points, n_contours = stroker.get_counts()
    with new_outline(n_points, n_contours) as stroked_outline:
        stroker.export(stroked_outline)
        bbox = stroked_outline.get_bbox()
        cbox = stroked_outline.get_cbox()
        assert (bbox.xMin, bbox.yMin, bbox.xMax, bbox.yMax) == \
            (746, -256, 7180, 9216)
        assert (cbox.xMin, cbox.yMin, cbox.xMax, cbox.yMax) == \
            (746, -256, 7180, 9216)
        assert stroked_outline.get_outside_border() == 0
        assert stroked_outline.get_inside_border() == 1
        assert len(stroked_outline.contours) == 2
        assert len(stroked_outline.points) == 225
        assert len(stroked_outline.tags) == 225

    border = outline.get_outside_border()
    n_points, n_contours = stroker.get_border_counts(border)
    with new_outline(n_points, n_contours) as outer_outline:
        stroker.export_border(border, outer_outline)
        bbox = outer_outline.get_bbox()
        cbox = outer_outline.get_cbox()
        assert (bbox.xMin, bbox.yMin, bbox.xMax, bbox.yMax) == \
            (746, -256, 7180, 9216)
        assert (cbox.xMin, cbox.yMin, cbox.xMax, cbox.yMax) == \
            (746, -256, 7180, 9216)
        assert outer_outline.get_outside_border() == 0
        assert outer_outline.get_inside_border() == 1
        assert len(outer_outline.contours) == 1
        assert len(outer_outline.points) == 121
        assert len(outer_outline.tags) == 121

    border = outline.get_inside_border()
    n_points, n_contours = stroker.get_border_counts(border)
    with new_outline(n_points, n_contours) as inner_outline:
        stroker.export_border(border, inner_outline)
        bbox = inner_outline.get_bbox()
        cbox = inner_outline.get_cbox()
        assert (bbox.xMin, bbox.yMin, bbox.xMax, bbox.yMax) == \
            (813, -128, 7052, 9088)
        assert (cbox.xMin, cbox.yMin, cbox.xMax, cbox.yMax) == \
            (813, -128, 7052, 9088)
        assert inner_outline.get_outside_border() == 1
        assert inner_outline.get_inside_border() == 0
        assert len(inner_outline.contours) == 1
        assert len(inner_outline.points) == 104
        assert len(inner_outline.tags) == 104
