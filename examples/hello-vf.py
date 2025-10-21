#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  Variable Font example - Copyright 2020 Josh Hadley, based on hello-world.py
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
from freetype import *

if __name__ == '__main__':
    import numpy
    import matplotlib.pyplot as plt

    face = Face('./SourceSansVariable-Roman.otf')
    text = 'Hello variable fonts!'
    face.set_char_size( 48*64 )
    slot = face.glyph
    face.set_var_design_coords((900,))  # set to widest for width calc.

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

    height *= 12

    Z = numpy.zeros((height,width), dtype=numpy.ubyte)

    # Second pass for actual rendering. Iterate through some weight axis values
    # and render the result, one per line.
    for i, wght in enumerate((900, 750, 675, 600, 500, 450, 325, 275, 100)):
        face.set_var_design_coords((wght,)) # set the weight axis value using "design coords"
        x, y = 0, 0
        previous = 0
        for c in text:
            face.load_char(c)
            bitmap = slot.bitmap
            top = slot.bitmap_top
            left = slot.bitmap_left
            w,h = bitmap.width, bitmap.rows
            y = (height - baseline - top) - (i * 48)
            kerning = face.get_kerning(face.get_char_index(previous), face.get_char_index(c))
            x += (kerning.x >> 6)
            Z[y:y+h,x+left:x+left+w] += numpy.array(bitmap.buffer, dtype='ubyte').reshape(h,w)
            x += (slot.advance.x >> 6)
            previous = c

    plt.figure(figsize=(10, 10*Z.shape[0]/float(Z.shape[1])))
    plt.imshow(Z, interpolation='nearest', origin='upper', cmap=plt.cm.gray)
    plt.xticks([]), plt.yticks([])
    plt.show()
