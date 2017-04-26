#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  pycairo/cairocffi-based glyph-mono/alpha example - Copyright 2017 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  rewrite of the numply,matplotlib-based example from Nicolas P. Rougier
#  - Not immitating the upside-downness of glyph-monochrome/glyph-alpha

#  This script default to normal(8-bit) rendering, but render to mono
#  if any argument is specified.
#
#  Mono rendering requires libtiff on small-endian platforms. See
#  comments in bitmap_to_surface.py.
#
# -----------------------------------------------------------------------------

'''
Glyph bitmap monochrome/alpha rendring
'''
from freetype import *

# use Matrix() from Cairo instead of from Freetype
from cairo import Context, ImageSurface, FORMAT_ARGB32, SurfacePattern, FILTER_BEST, Matrix
from bitmap_to_surface import make_image_surface

if __name__ == '__main__':
    from PIL import Image
    import sys

    face = Face('./Vera.ttf')
    face.set_char_size( 48*64 )

    if len(sys.argv) < 2:
        # Normal(8-bit) Rendering
        face.load_char('S', FT_LOAD_RENDER |
                       FT_LOAD_TARGET_NORMAL )
    else:
        # Mono(1-bit) Rendering
        face.load_char('S', FT_LOAD_RENDER |
                       FT_LOAD_TARGET_MONO )

    bitmap = face.glyph.bitmap
    width  = face.glyph.bitmap.width
    rows   = face.glyph.bitmap.rows
    pitch  = face.glyph.bitmap.pitch

    glyph_surface = make_image_surface(face.glyph.bitmap)

    surface = ImageSurface(FORMAT_ARGB32, 800, 600)
    ctx = Context(surface)
    ctx.rectangle(0,0,800,600)
    ctx.set_line_width(0)
    ctx.set_source_rgb (0.5 , 0.5, 0.5)
    ctx.fill()
    #
    scale = 480.0 / rows
    ctx.set_source_surface(glyph_surface, 0, 0)
    pattern = ctx.get_source()
    SurfacePattern.set_filter(pattern, FILTER_BEST)
    scalematrix = Matrix()
    scalematrix.scale(1.0/scale,1.0/scale)
    scalematrix.translate(-(400.0 - width *scale /2.0 ), -60)
    pattern.set_matrix(scalematrix)
    ctx.set_source_rgb (0 , 0, 1)
    ctx.mask(pattern)
    ctx.fill()
    surface.flush()
    surface.write_to_png("glyph-mono+alpha-cairo.png")
    Image.open("glyph-mono+alpha-cairo.png").show()
