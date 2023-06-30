#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pycairo/cairocffi-based emoji-color example - Copyright 2017-2023 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  This script demonstrates overlapping emojis.
#
#  Note: On Mac OS X before Sierra (10.12), change ttc->ttf;
#        try Google's NotoColorEmoji.ttf at size 109 on Linux.
#
#  Updated 2023, now somewhat specific to pycairo and CPython 3.3+,
#  and also small-endian (from FORMAT_ARGB32 vs FT_PIXEL_MODE_BGRA),
#  but no longer needs numpy.
#
#  Older 2017 version (depends on numpy):
#  Limitation: Suface.get_data() is not in the "python 3, pycairo < 1.11" combo.

import freetype
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

if ( face.glyph.bitmap.pitch != width * 4 ):
    raise RuntimeError('pitch != width * 4 for color bitmap: Please report this.')

# See https://stackoverflow.com/questions/59574816/obtaining-a-memoryview-object-from-a-ctypes-c-void-p-object
from ctypes import pythonapi, c_char_p, c_ssize_t, c_int, py_object, cast
pythonapi.PyMemoryView_FromMemory.argtypes = (c_char_p, c_ssize_t, c_int)
pythonapi.PyMemoryView_FromMemory.restype = py_object
I = ImageSurface.create_for_data( pythonapi.PyMemoryView_FromMemory(cast(bitmap._FT_Bitmap.buffer, c_char_p),
                                                                    bitmap.rows * bitmap.pitch,
                                                                    0x200), # Read-Write
                                        FORMAT_ARGB32,
                                        width, rows,
                                        bitmap.pitch )
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
