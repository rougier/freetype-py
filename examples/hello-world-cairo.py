#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  pycairo/cairocffi-based "Hello World" example - Copyright 2017 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  rewrite of the numply,matplotlib-based example from Nicolas P. Rougier
#
# -----------------------------------------------------------------------------
from freetype import *

from cairo import Context, ImageSurface, FORMAT_A8
from bitmap_to_surface import make_image_surface

if __name__ == '__main__':
    from PIL import Image

    face = Face('./Vera.ttf')
    text = 'Hello World !'
    face.set_char_size( 48*64 )
    slot = face.glyph

    # First pass to compute bbox
    width, height, baseline = 0, 0, 0
    previous = 0
    for i,c in enumerate(text):
        face.load_char(c)
        bitmap = slot.bitmap
        height = max(height,
                     bitmap.rows + max(0,-(slot.bitmap_top-bitmap.rows)))
        baseline = max(baseline, max(0,-(slot.bitmap_top-bitmap.rows)))
        kerning = face.get_kerning(face.get_char_index(previous), face.get_char_index(c))
        width += (slot.advance.x >> 6) + (kerning.x >> 6)
        previous = c

    Z = ImageSurface(FORMAT_A8, width, height)
    ctx = Context(Z)

    # Second pass for actual rendering
    x, y = 0, 0
    previous = 0
    for c in text:
        face.load_char(c)
        bitmap = slot.bitmap
        top = slot.bitmap_top
        left = slot.bitmap_left
        w,h = bitmap.width, bitmap.rows
        y = height-baseline-top
        kerning = face.get_kerning(face.get_char_index(previous), face.get_char_index(c))
        x += (kerning.x >> 6)
        # cairo does not like zero-width bitmap from the space character!
        if (bitmap.width > 0):
            glyph_surface = make_image_surface(face.glyph.bitmap)
            ctx.set_source_surface(glyph_surface, x+left, y)
            ctx.paint()
        x += (slot.advance.x >> 6)
        previous = c
    Z.flush()
    Z.write_to_png("hello-world-cairo.png")
    Image.open("hello-world-cairo.png").show()
