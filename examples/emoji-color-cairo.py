#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pycairo/cairocffi-based emoji-color example - Copyright 2017 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  This script demonstrates overlapping emojis.
#
#  Note: On Mac OS X before Sierra (10.12), change ttc->ttf;
#        try Google's NotoColorEmoji.ttf at size 109 on Linux.
#
#  Limitation: Suface.get_data() is not in the "python 3, pycairo < 1.11" combo.

import freetype
import numpy as np
from PIL import Image

from cairo import ImageSurface, FORMAT_ARGB32, Context

face = freetype.Face("/System/Library/Fonts/Apple Color Emoji.ttc")
# Not all char sizes are valid for emoji fonts;
# Google's NotoColorEmoji only accept size 109 to get 136x128 bitmaps
face.set_char_size( 160*64 )
face.load_char('😀', freetype.FT_LOAD_COLOR)

bitmap = face.glyph.bitmap
width = face.glyph.bitmap.width
rows = face.glyph.bitmap.rows

# The line below depends on this assumption. Check.
if ( face.glyph.bitmap.pitch != width * 4 ):
    raise RuntimeError('pitch != width * 4 for color bitmap: Please report this.')
bitmap = np.array(bitmap.buffer, dtype=np.uint8).reshape((bitmap.rows,bitmap.width,4))

I = ImageSurface(FORMAT_ARGB32, width, rows)
try:
    ndI = np.ndarray(shape=(rows,width), buffer=I.get_data(),
                     dtype=np.uint32, order='C',
                     strides=[I.get_stride(), 4])
except NotImplementedError:
    raise SystemExit("For python 3.x, you need pycairo >= 1.11+ (from https://github.com/pygobject/pycairo)")

# Although both are 32-bit, cairo is host-order while
# freetype is small endian.
ndI[:,:] = bitmap[:,:,3] * 2**24 + bitmap[:,:,2] * 2**16 + bitmap[:,:,1] * 2**8 + bitmap[:,:,0]
I.mark_dirty()

surface = ImageSurface(FORMAT_ARGB32, 2*width, rows)
ctx = Context(surface)

ctx.set_source_surface(I, 0, 0)
ctx.paint()

ctx.set_source_surface(I, width/2, 0)
ctx.paint()

ctx.set_source_surface(I, width , 0)
ctx.paint()

surface.write_to_png("emoji-color-cairo.png")
Image.open("emoji-color-cairo.png").show()
