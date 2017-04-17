#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import freetype
import numpy as np
from PIL import Image

def convert_bgra_to_rgb(buf):
    blue = buf[:,:,0]
    green = buf[:,:,1]
    red = buf[:,:,2]
    return np.dstack((red, green, blue))

face = freetype.Face("/System/Library/Fonts/Apple Color Emoji.ttc")
face.set_char_size( 20*64 )
face.load_char('😀', freetype.FT_LOAD_COLOR)
bitmap = face.glyph.bitmap
bitmap = np.array(bitmap.buffer, dtype=np.uint8).reshape((bitmap.rows,bitmap.width,4))
rgb = convert_bgra_to_rgb(bitmap)
im = Image.fromarray(rgb)
im.show()
