#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  OT-SVG example, alternative version based on Skia
#
#  Copyright 2023 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.

#  See also the other one, the rsvg-based OT-SVG example.

# "ot-svg-draw-skia.py" was written based on skia m87.
# This example requires m117, and also accelerated GL integration;
# should work on any OT-SVG font, unlike "ot-svg-draw-skia.py".

if __name__ == '__main__':
    import sys

    from ctypes import byref, pythonapi, cast, c_char_p
    from freetype import Face, get_handle, FT_Property_Set, FT_LOAD_COLOR, FT_LOAD_RENDER
    from OpenGL import GL
    import glfw
    import skia
    from skia import ImageInfo, ColorType, AlphaType

    from skia_ot_svg_module import hooks
    from skia_glfw_module import glfw_window, skia_surface

    execname = sys.argv[0]

    if len(sys.argv) < 2:
        print("Example usage: %s TrajanColor-Concept.otf" % execname)
        exit(1)

    face = Face(sys.argv[1])

    face.set_char_size( 160*64 )
    library = get_handle()

    FT_Property_Set( library, b"ot-svg", b"svg-hooks", byref(hooks) ) # python 3 only syntax
    face.load_char('A', FT_LOAD_COLOR | FT_LOAD_RENDER )

    bitmap = face.glyph.bitmap
    width = face.glyph.bitmap.width
    rows = face.glyph.bitmap.rows

    if ( face.glyph.bitmap.pitch != width * 4 ):
        raise RuntimeError('pitch != width * 4 for color bitmap: Please report this.')

    WIDTH, HEIGHT = 2*width, rows

    glyphBitmap = skia.Bitmap()
    glyphBitmap.setInfo(ImageInfo.Make(bitmap.width, bitmap.rows,
                                       ColorType.kBGRA_8888_ColorType,
                                       AlphaType.kPremul_AlphaType),
                        bitmap.pitch)
    glyphBitmap.setPixels(pythonapi.PyMemoryView_FromMemory(cast(bitmap._FT_Bitmap.buffer, c_char_p),
                                                            bitmap.rows * bitmap.pitch,
                                                            0x200), # Read-Write
                          )

    with glfw_window(WIDTH, HEIGHT) as window:
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        with skia_surface(window) as surface:
            with surface as canvas:
                canvas.drawBitmap(glyphBitmap, 0, 0)
                canvas.drawBitmap(glyphBitmap, width/2, 0)
                canvas.drawBitmap(glyphBitmap, width, 0)
                surface.flushAndSubmit()
                glfw.swap_buffers(window)

            while (glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS
                   and not glfw.window_should_close(window)):
                glfw.wait_events()
