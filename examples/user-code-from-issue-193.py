#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Corrected version of user-submitted code in https://github.com/rougier/freetype-py/issues/193

# Comments:
#     The original version missed "freetype.FT_LOAD_RENDER" and
#     "freetype.FT_LOAD_TARGET_MONO", and also has the unfortunate
#     setting of pixel size "16". Thus for some glyphs on 'simsun.ttc',
#     the code returns the embedded bitmap, while for other glyphs without
#     embedded bitmaps, it returns garbage for the bitmap buffer
#     (if you do not check "font.glyph.format" and "font.glyph.bitmap.pixel_mode" ;
#     font.glyph.format == FT_GLYPH_FORMAT_OUTLINE in that case). "bitmap.pitch" was also
#     not used in the original, and hard-coded length of scanline was used.

import freetype

font = freetype.Face(r"simsun.ttc")

# 绘制字符
font.set_pixel_sizes(19, 19)
font.load_char('1', freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO)
#font.load_char('字', freetype.FT_LOAD_RENDER | freetype.FT_LOAD_TARGET_MONO)
bitmap = font.glyph.bitmap
print(bitmap.rows, bitmap.width, bitmap.pitch)
assert(font.glyph.format == freetype.FT_GLYPH_FORMAT_BITMAP)
assert(font.glyph.bitmap.pixel_mode == freetype.FT_PIXEL_MODE_MONO)
print(bitmap.buffer)
print(len(bitmap.buffer))
left = []
right = []
for b, j in enumerate(bitmap.buffer):
    b_res = list(format(j, "08b"))
    for r in b_res:
        if r == "1":
            print("\033[1;30;46m   \033[0m", end="")
        else:
            print("\033[1;30;40m   \033[0m", end="")
    if (b + 1) % bitmap.pitch == 0 and b > 0:
        right.append(format(j, "02X"))
        print()
    else:
        left.append(format(j, "02X"))
print(' '.join(left))
print(' '.join(right))
