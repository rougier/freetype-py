#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
from freetype import *

if __name__ == '__main__':
    import numpy
    import matplotlib.pyplot as plt

    face = Face('./Vera.ttf')
    text = 'Hello World !'
    fontsize = 48
    face.set_char_size( fontsize*64 )
    slot = face.glyph

    # First pass to compute bbox
    width = 0
    top = -fontsize #The distance from baseline to the top row of the bbox
    bot = fontsize #The distance from baseline to the bottom row of the bbox (may be negative)
    previous = 0
    for i,c in enumerate(text):
        face.load_char(c)
        bitmap = slot.bitmap
        top = max(top, slot.bitmap_top)
        bot = min(bot, slot.bitmap_top - bitmap.rows)
        kerning = face.get_kerning(face.get_char_index(previous), face.get_char_index(c))
        width += (slot.advance.x >> 6) + (kerning.x >> 6)
        previous = c

    height = top - bot
    Z = numpy.zeros((height,width), dtype=numpy.ubyte)

    # Second pass for actual rendering
    x, y = 0, 0
    previous = 0
    for c in text:
        face.load_char(c)
        bitmap = slot.bitmap
        w,h = bitmap.width, bitmap.rows
        y = top - slot.bitmap_top
        kerning = face.get_kerning(face.get_char_index(previous), face.get_char_index(c))
        x += (kerning.x >> 6)
        Z[y:y+h,x+left:x+left+w] += numpy.array(bitmap.buffer, dtype='ubyte').reshape(h,w)
        x += (slot.advance.x >> 6)
        previous = c

    plt.figure(figsize=(10, 10*Z.shape[0]/float(Z.shape[1])))
    plt.imshow(Z, interpolation='nearest', origin='upper', cmap=plt.cm.gray)
    plt.xticks([]), plt.yticks([])
    plt.show()
