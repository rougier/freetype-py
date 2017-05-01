#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  pycairo/cairocffi-based emoji-color example - Copyright 2017 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  This script demonstrates overlapping emojis.
#

import freetype
import numpy as np
from PIL import Image

from cairo import ImageSurface, FORMAT_ARGB32, Context

face = freetype.Face("Apple Color Emoji.ttf")
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
ndI = np.ndarray(shape=(rows,width), buffer=I.get_data(),
                 dtype=np.uint32, order='C',
                 strides=[I.get_stride(), 4])

# Although both are 32-bit, cairo is host-order while
# freetype is small endian.
ndI[:,:] = bitmap[:,:,3] * 16777216 + bitmap[:,:,2] * 65536 + bitmap[:,:,1] * 256 + bitmap[:,:,0]
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
