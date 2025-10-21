#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  pycairo/cairocffi-based wordle example - Copyright 2017 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  rewrite of the numply,matplotlib-based example from Nicolas P. Rougier
#  - Cairo can paint partly off-screen, so this example does!
#
#  This example behaves differently under pycairo 1.11+ (released in 2017-04-09).
#  Auto-checked. On older pycairo, it does not draw partial patterns at the edges.
#  Also, Suface.get_data() is not in the "python 3, pycairo < 1.11" combination.
#
# -----------------------------------------------------------------------------
from math import cos, sin
from numpy import random, sort, sqrt, ndarray, ubyte
from freetype import *

try:
    # pycairo 1.11+:
    from cairo import Region, RectangleInt, REGION_OVERLAP_OUT
except ImportError:
    # stubs for pycairo < 1.11:
    class Region:
        def __init__(self):
            return
        def union(self, rec):
            return
        def contains_rectangle(self, rec):
            # inhibit drawing
            return True
    class RectangleInt:
        def __init__(self, x, y, w, h):
            return
    REGION_OVERLAP_OUT = False

from cairo import Context, ImageSurface, FORMAT_A8, FORMAT_ARGB32, Matrix
from bitmap_to_surface import make_image_surface

def make_label(text, filename, size=12, angle=0):
    '''
    Parameters:
    -----------
    text : string
        Text to be displayed
    filename : string
        Path to a font
    size : int
        Font size in 1/64th points
    angle : float
        Text angle in degrees
    '''
    face = Face(filename)
    face.set_char_size( size*64 )
    # FT_Angle is a 16.16 fixed-point value expressed in degrees.
    angle = FT_Angle(angle * 65536)
    matrix  = FT_Matrix( FT_Cos( angle ),
                         - FT_Sin( angle ),
                         FT_Sin( angle ) ,
                         FT_Cos( angle ) )
    flags = FT_LOAD_RENDER
    pen = FT_Vector(0,0)
    FT_Set_Transform( face._FT_Face, byref(matrix), byref(pen) )
    previous = 0
    xmin, xmax = 0, 0
    ymin, ymax = 0, 0
    for c in text:
        face.load_char(c, flags)
        kerning = face.get_kerning(face.get_char_index(previous), face.get_char_index(c))
        previous = c
        bitmap = face.glyph.bitmap
        pitch  = face.glyph.bitmap.pitch
        width  = face.glyph.bitmap.width
        rows   = face.glyph.bitmap.rows
        top    = face.glyph.bitmap_top
        left   = face.glyph.bitmap_left
        pen.x += kerning.x
        x0 = (pen.x >> 6) + left
        x1 = x0 + width
        y0 = (pen.y >> 6) - (rows - top)
        y1 = y0 + rows
        xmin, xmax = min(xmin, x0),  max(xmax, x1)
        ymin, ymax = min(ymin, y0), max(ymax, y1)
        pen.x += face.glyph.advance.x
        pen.y += face.glyph.advance.y

    L = ImageSurface(FORMAT_A8, xmax-xmin, ymax-ymin)
    previous = 0
    pen.x, pen.y = 0, 0
    ctx = Context(L)
    for c in text:
        face.load_char(c, flags)
        kerning = face.get_kerning(face.get_char_index(previous), face.get_char_index(c))
        previous = c
        bitmap = face.glyph.bitmap
        pitch  = face.glyph.bitmap.pitch
        width  = face.glyph.bitmap.width
        rows   = face.glyph.bitmap.rows
        top    = face.glyph.bitmap_top
        left   = face.glyph.bitmap_left
        pen.x += kerning.x
        x = (pen.x >> 6) - xmin + left
        y = - (pen.y >> 6) + ymax - top
        if (width > 0):
            glyph_surface = make_image_surface(face.glyph.bitmap)
            ctx.set_source_surface(glyph_surface, x, y)
            ctx.paint()
        pen.x += face.glyph.advance.x
        pen.y += face.glyph.advance.y

    L.flush()
    return L


if __name__ == '__main__':
    from PIL import Image

    n_words = 200
    H, W, dpi = 600, 800, 72.0
    I = ImageSurface(FORMAT_A8, W, H)
    ctxI = Context(I)
    ctxI.rectangle(0,0,800,600)
    ctxI.set_source_rgba (0.9, 0.9, 0.9, 0)
    ctxI.fill()
    S = random.normal(0,1,n_words)
    S = (S-S.min())/(S.max()-S.min())
    S = sort(1-sqrt(S))[::-1]
    sizes = (12 + S*48).astype(int).tolist()

    def spiral():
        eccentricity = 1.5
        radius = 8
        step = 0.1
        t = 0
        while True:
            t += step
            yield eccentricity*radius*t*cos(t), radius*t*sin(t)

    drawn_regions = Region()
    for size in sizes:
        angle = random.randint(-25,25)
        try:
            L = make_label('Hello', './Vera.ttf', size, angle=angle)
        except NotImplementedError:
            raise SystemExit("For python 3.x, you need pycairo >= 1.11+ (from https://github.com/pygobject/pycairo)")
        h = L.get_height()
        w = L.get_width()
        if h < H and w < W:
            x0 = W//2 + (random.uniform()-.1)*50
            y0 = H//2 + (random.uniform()-.1)*50
            for dx,dy in spiral():
                c = .25+.75*random.random()
                x = int(x0+dx)
                y = int(y0+dy)
                checked = False
                I.flush()
                if not (x <= w//2 or y <= h//2 or x >= (W-w//2) or y >= (H-h//2)):
                    ndI = ndarray(shape=(h,w), buffer=I.get_data(), dtype=ubyte, order='C',
                                  offset=(x-w//2) + I.get_stride() * (y-h//2),
                                  strides=[I.get_stride(), 1])
                    ndL = ndarray(shape=(h,w), buffer=L.get_data(), dtype=ubyte, order='C',
                                  strides=[L.get_stride(), 1])
                    if ((ndI * ndL).sum() == 0):
                       checked = True
                new_region = RectangleInt(x-w//2, y-h//2, w, h)
                if  (checked or ( drawn_regions.contains_rectangle(new_region) == REGION_OVERLAP_OUT )):
                    ctxI.set_source_surface(L, 0, 0)
                    pattern = ctxI.get_source()
                    scalematrix = Matrix()
                    scalematrix.scale(1.0,1.0)
                    scalematrix.translate(w//2 - x, h//2 - y)
                    pattern.set_matrix(scalematrix)
                    ctxI.set_source_rgba(c,c,c,c)
                    ctxI.mask(pattern)
                    drawn_regions.union(new_region)
                    break
    I.flush()
    I.write_to_png("wordle-cairo.png")
    Image.open("wordle-cairo.png").show()
