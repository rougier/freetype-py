#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  pycairo/cairocffi-based glyph-outline example - Copyright 2017 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  rewrite of the numply,matplotlib-based example from Nicolas P. Rougier
#
# -----------------------------------------------------------------------------
'''
Glyph outline rendering
'''
from freetype import *

# using Matrix class from Cairo, instead of FreeType's
from cairo import Context, ImageSurface, FORMAT_ARGB32, SurfacePattern, FILTER_BEST, Matrix
from bitmap_to_surface import make_image_surface

if __name__ == '__main__':
    from PIL import Image

    face = Face('./Vera.ttf')
    face.set_char_size( 4*48*64 )
    flags = FT_LOAD_DEFAULT | FT_LOAD_NO_BITMAP
    face.load_char('S', flags )
    slot = face.glyph
    glyph = slot.get_glyph()
    stroker = Stroker( )
    stroker.set(64, FT_STROKER_LINECAP_ROUND, FT_STROKER_LINEJOIN_ROUND, 0 )
    glyph.stroke( stroker , True )
    blyph = glyph.to_bitmap(FT_RENDER_MODE_NORMAL, Vector(0,0), True )
    bitmap = blyph.bitmap
    width, rows, pitch = bitmap.width, bitmap.rows, bitmap.pitch
    surface = ImageSurface(FORMAT_ARGB32, 600, 800)
    ctx = Context(surface)
    Z = make_image_surface(bitmap)
    ctx.set_source_surface(Z, 0, 0)
    scale = 640.0 / rows
    patternZ = ctx.get_source()
    SurfacePattern.set_filter(patternZ, FILTER_BEST)
    scalematrix = Matrix()
    scalematrix.scale(1.0/scale,1.0/scale)
    scalematrix.translate(-(300.0 - width *scale /2.0 ), -80)
    patternZ.set_matrix(scalematrix)
    ctx.set_source_rgb (0 , 0, 1)
    ctx.mask(patternZ)
    ctx.fill()
    surface.flush()
    surface.write_to_png("glyph-outline-cairo.png")
    Image.open("glyph-outline-cairo.png").show()
