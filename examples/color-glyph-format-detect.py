#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Identify the color glyph format.
#
#  Copyright 2023 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  Note:
#      This is a per-glyph property.
#
#      Glyph 1426 in SEGUIEMJ.TTF is a glyph layer of glyph 1425.
#      Glyph 1426 is a plain outline, 1425 is a COLRv0 glyph.
#
#      Noto Color Emoji is only valid for size 109.
#
#      Apple Color Emoji works for size 160 and a few other specific sizes.
#
#      SVG and COLRv1 is not exclusive - some fonts have both.

from freetype import *

if __name__ == '__main__':
    import sys
    execname = sys.argv[0]

    if len(sys.argv) < 3:
        print("Example usage: %s TrajanColor-Concept.otf <glyph_id> [size]" % execname)
        exit(1)

    face = Face(sys.argv[1])

    glyph_id = c_uint(int(sys.argv[2]))

    if (len(sys.argv) > 3):
        size = int(sys.argv[3])
    else:
        size = 160

    face.set_char_size( size*64 )
    face.load_glyph( glyph_id, FT_LOAD_COLOR )

    print("glyph id %d is " % (glyph_id.value), end='')
    
    if (face.glyph.format == FT_GLYPH_FORMAT_SVG):
        print("SVG; ", end='')
    if (face.glyph.format == FT_GLYPH_FORMAT_BITMAP):
        print("Bitmap; ", end='')
    if (face.glyph.format == FT_GLYPH_FORMAT_OUTLINE):
        print("Outline; ", end='')

    opaqueLayerPaint = FT_OpaquePaint(None, 1)
    if (FT_Get_Color_Glyph_Paint(face._FT_Face, glyph_id,
                                 FT_COLOR_INCLUDE_ROOT_TRANSFORM,
                                 byref(opaqueLayerPaint))):
        print("COLRv1; ", end='')
    else:
        layerGlyphIndex = FT_UInt(0)
        layerColorIndex = FT_UInt(0)
        layerIterator   = FT_LayerIterator( 0, 0, None )
        layer_count = 0
        if (FT_Get_Color_Glyph_Layer(face._FT_Face, glyph_id,
                                     byref(layerGlyphIndex),
                                     byref(layerColorIndex),
                                     byref(layerIterator))):
            if (layerGlyphIndex.value != 0):
                print("COLRv0; ", end='')

    print ("") # line ending
