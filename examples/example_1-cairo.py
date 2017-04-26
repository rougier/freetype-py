#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  pycairo/cairocffi-based FreeType example - Copyright 2017 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  rewrite of the numply,matplotlib-based example from Nicolas P. Rougier
#
# -----------------------------------------------------------------------------
#
# Direct translation of example 1 from the freetype tutorial:
# http://www.freetype.org/freetype2/docs/tutorial/step1.html
#
# Except we uses FreeType's own trigonometric functions instead of those
# from the system/python's math library.


from cairo import Context, ImageSurface, FORMAT_A8
from bitmap_to_surface import make_image_surface

from freetype.raw import *
from PIL import Image

WIDTH, HEIGHT = 640, 480
image = ImageSurface(FORMAT_A8, WIDTH, HEIGHT)
ctx = Context(image)

def to_c_str(text):
    ''' Convert python strings to null terminated c strings. '''
    cStr = create_string_buffer(text.encode(encoding='UTF-8'))
    return cast(pointer(cStr), POINTER(c_char))

def draw_bitmap( bitmap, x, y):
    global image, ctx
    # cairo does not like zero-width surface
    if (bitmap.width > 0):
        glyph_surface = make_image_surface(bitmap)
        ctx.set_source_surface(glyph_surface, x, y)
        ctx.paint()

def main():

    library = FT_Library()
    matrix  = FT_Matrix()
    face    = FT_Face()
    pen     = FT_Vector()
    filename= 'Vera.ttf'
    text    = 'Hello World !'
    num_chars = len(text)
    # FT_Angle is a 16.16 fixed-point value expressed in degrees.
    angle   = FT_Angle(25 * 65536)

    # initialize library, error handling omitted
    error = FT_Init_FreeType( byref(library) )

    # create face object, error handling omitted
    error = FT_New_Face( library, to_c_str(filename), 0, byref(face) )


    # set character size: 50pt at 100dpi, error handling omitted
    error = FT_Set_Char_Size( face, 50 * 64, 0, 100, 0 )
    slot = face.contents.glyph

    # set up matrix
    matrix.xx = FT_Cos( angle )
    matrix.xy = - FT_Sin( angle )
    matrix.yx = FT_Sin( angle )
    matrix.yy = FT_Cos( angle )

    # the pen position in 26.6 cartesian space coordinates; */
    # start at (300,200) relative to the upper left corner  */
    pen.x = 200 * 64;
    pen.y = ( HEIGHT - 300 ) * 64

    for n in range(num_chars):
        # set transformation
        FT_Set_Transform( face, byref(matrix), byref(pen) )

        # load glyph image into the slot (erase previous one)
        charcode = ord(text[n])
        index = FT_Get_Char_Index( face, charcode )
        FT_Load_Glyph( face, index, FT_LOAD_RENDER )

        # now, draw to our target surface (convert position)
        draw_bitmap( slot.contents.bitmap,
                     slot.contents.bitmap_left,
                     HEIGHT - slot.contents.bitmap_top )

        # increment pen position
        pen.x += slot.contents.advance.x
        pen.y += slot.contents.advance.y

    FT_Done_Face(face)
    FT_Done_FreeType(library)

    image.flush()
    image.write_to_png("example_1-cairo.png")
    Image.open("example_1-cairo.png").show()


if __name__ == '__main__':
    main()
