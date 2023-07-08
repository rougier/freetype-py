#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  OT-SVG example with Skia
#
#  Copyright 2023 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.

# Limitation:
#     Skia-python bundles with Skia m87 (at time of writing this).
#
#     Skia m88 is first version where SkSVG* is considered no longer experimental.
#
#     Skia m103 is the first Skia build which contains 9cbadcd9280dc139af2f4d41d25a6c9a750e0302.
#     That introduces "SkSVGDOM::renderNode()" among other stuff,
#     necessary for rendering "some" OT-SVG fonts. Guess what, that commit
#     is titled "Add optional OT-SVG support to FreeType"!
#
#     So the example below only works correctly for "some" glyphs in
#     "some other" OT-SVG fonts, and also with very limited functionality
#     beyond what is used below.
#
#     The missing functionality (and support for beyond Skia m103) is filed
#     as skia-python issue #192.

from freetype import *

import skia

if __name__ == '__main__':
    import sys
    execname = sys.argv[0]

    if len(sys.argv) < 2:
        print("Example usage: %s TrajanColor-Concept.otf" % execname)
        exit(1)

    face = Face(sys.argv[1])

    face.set_char_size( 160*64 )
    face.load_char('A', FT_LOAD_COLOR )
    slot = face.glyph._FT_GlyphSlot

    if (face.glyph.format == FT_GLYPH_FORMAT_SVG):
        document = ctypes.cast(slot.contents.other, FT_SVG_Document)
        doc = ctypes.string_at(document.contents.svg_document, # not terminated
                               size=document.contents.svg_document_length)
        d = skia.Data(doc)
        m = skia.MemoryStream(d)
        h = skia.SVGDOM.MakeFromStream(m)

        WIDTH, HEIGHT = 160, 160
        
        size = skia.Size()
        size.fHeight = WIDTH
        size.fWidth = HEIGHT
        
        h.setContainerSize(size)

        surface = skia.Surface(WIDTH * 2, HEIGHT)
        
        with surface as canvas:
            canvas.translate(0,HEIGHT)
            h.render(canvas)
            canvas.translate(WIDTH/4,0)
            h.render(canvas)
            canvas.translate(WIDTH/4,0)
            h.render(canvas)
            canvas.translate(WIDTH/4,0)
            h.render(canvas)
            canvas.translate(WIDTH/4,0)
            h.render(canvas)
            canvas.translate(WIDTH/4,0)
            h.render(canvas)
            
            surface.flushAndSubmit()
            image = surface.makeImageSnapshot()
            image.save("ot-svg-draw-skia.png", skia.kPNG)

        from PIL import Image
        Image.open("ot-svg-draw-skia.png").show()

    else:
        print("Not SVG glyph.format")
