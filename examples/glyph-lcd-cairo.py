#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  pycairo/cairocffi-based glyph-lcd example - Copyright 2017 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  rewrite of the numply,matplotlib-based example from Nicolas P. Rougier
#  - Not immitating the upside-downness
#  - Do LCD_V side by side also
#
#  Limitation: Suface.get_data() is not in the "python 3, pycairo < 1.11" combo.
#
# -----------------------------------------------------------------------------
'''
Glyph bitmap LCD display (sub-pixel) rendering
'''
from freetype import *
# use Matrix() from Cairo instead of from Freetype
from cairo import Context, ImageSurface, FORMAT_ARGB32, SurfacePattern, FILTER_BEST, Matrix

if __name__ == '__main__':
    from PIL import Image
    from numpy import ndarray, ubyte, uint32

    face = Face('./Vera.ttf')
    face.set_char_size( 48*64 )
    face.load_char('S', FT_LOAD_RENDER |
                        FT_LOAD_TARGET_LCD )
    bitmap = face.glyph.bitmap
    width  = face.glyph.bitmap.width//3
    rows   = face.glyph.bitmap.rows
    pitch  = face.glyph.bitmap.pitch
    copybuffer = (c_ubyte * (pitch * rows))()
    memmove(pointer(copybuffer), bitmap._FT_Bitmap.buffer,
            pitch * rows)

    I = ImageSurface(FORMAT_ARGB32, width, rows)
    ndR = ndarray(shape=(rows,width), buffer=copybuffer,
                  dtype=ubyte, order='C',
                  offset=0,
                  strides=[pitch, 3])
    ndG = ndarray(shape=(rows,width), buffer=copybuffer,
                  dtype=ubyte, order='C',
                  offset=1,
                  strides=[pitch, 3])
    ndB = ndarray(shape=(rows,width), buffer=copybuffer,
                  dtype=ubyte, order='C',
                  offset=2,
                  strides=[pitch, 3])
    try:
        ndI = ndarray(shape=(rows,width), buffer=I.get_data(),
                      dtype=uint32, order='C',
                      strides=[I.get_stride(), 4])
    except NotImplementedError:
       raise SystemExit("For python 3.x, you need pycairo >= 1.11+ (from https://github.com/pygobject/pycairo)")
    # 255 * 2**24 = opaque
    ndI[:,:] = 255 * 2**24 + ndR[:,:] * 2**16 + ndG[:,:] * 2**8 + ndB[:,:]
    I.mark_dirty()

    surface = ImageSurface(FORMAT_ARGB32, 800, 600)
    ctx = Context(surface)

    ctx.set_source_surface(I, 0, 0)
    pattern = ctx.get_source()
    SurfacePattern.set_filter(pattern, FILTER_BEST)
    scale = 480.0 / rows
    scalematrix = Matrix()
    scalematrix.scale(1.0/scale,1.0/scale)
    scalematrix.translate(-(400.0 - width *scale /2.0 )+200, -60)
    pattern.set_matrix(scalematrix)
    ctx.paint()

    # we need this later for shifting the taller LCD_V glyph up.
    rows_old = rows

    # LCD_V
    face.load_char('S', FT_LOAD_RENDER |
                        FT_LOAD_TARGET_LCD_V )
    bitmap = face.glyph.bitmap
    width  = face.glyph.bitmap.width
    rows   = face.glyph.bitmap.rows//3
    pitch  = face.glyph.bitmap.pitch
    copybuffer = (c_ubyte * (pitch * face.glyph.bitmap.rows))()
    memmove(pointer(copybuffer), bitmap._FT_Bitmap.buffer,
            pitch * face.glyph.bitmap.rows)

    I = ImageSurface(FORMAT_ARGB32, width, rows)
    ndR = ndarray(shape=(rows,width), buffer=copybuffer,
                  dtype=ubyte, order='C',
                  offset=0,
                  strides=[pitch*3, 1])
    ndG = ndarray(shape=(rows,width), buffer=copybuffer,
                  dtype=ubyte, order='C',
                  offset=pitch,
                  strides=[pitch*3, 1])
    ndB = ndarray(shape=(rows,width), buffer=copybuffer,
                  dtype=ubyte, order='C',
                  offset=2*pitch,
                  strides=[pitch*3, 1])
    ndI = ndarray(shape=(rows,width), buffer=I.get_data(),
                  dtype=uint32, order='C',
                  strides=[I.get_stride(), 4])
    # 255 * 2**24 = opaque
    ndI[:,:] = 255 * 2**24 + ndR[:,:] * 2**16 + ndG[:,:] * 2**8 + ndB[:,:]
    I.mark_dirty()

    ctx.set_source_surface(I, 0, 0)
    pattern = ctx.get_source()
    SurfacePattern.set_filter(pattern, FILTER_BEST)
    # Re-use the sane scale (LVD_V taller than LCD),
    # but adjust vertical position to line up mid-height of glyphs
    adjust = (rows - rows_old) * 240.0 /rows
    scalematrix.translate(-400, adjust)
    pattern.set_matrix(scalematrix)
    ctx.paint()
    #
    surface.flush()
    surface.write_to_png("glyph-lcd-cairo.png")
    Image.open("glyph-lcd-cairo.png").show()
