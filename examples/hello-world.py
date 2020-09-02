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
    text = 'Hello World, !'
    face.set_char_size( 48*64 )
    slot = face.glyph

    # First pass to compute bbox
    width = 0
    top = -32768
    bot = 32767
    previous = 0
    for i,c in enumerate(text):
        face.load_char(c)
        bitmap = slot.bitmap
        top = max(top, slot.bitmap_top)
        bot = min(bot, slot.bitmap_top - bitmap.rows)
        kerning = face.get_kerning(previous, c)
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
        kerning = face.get_kerning(previous, c)
        x += (kerning.x >> 6)
        Z[y:y+h,x:x+w] += numpy.array(bitmap.buffer, dtype='ubyte').reshape(h,w)
        x += (slot.advance.x >> 6)
        previous = c

    plt.figure(figsize=(10, 10*Z.shape[0]/float(Z.shape[1])))
    plt.imshow(Z, interpolation='nearest', origin='upper', cmap=plt.cm.gray)
    plt.xticks([]), plt.yticks([])
    plt.show()
