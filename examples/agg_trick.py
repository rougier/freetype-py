# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
from freetype import *

if __name__ == '__main__':
    import numpy as np
    import Image

    W,H = 650, 240
    Z = np.zeros( (H,W), dtype=np.ubyte )
    text = "A Quick Brown Fox Jumps Over The Lazy Dog 0123456789"
    face = Face('./Vera.ttf')

    pen = Vector(10*64, (H-10)*64)
    for size in range(8,22):
        face.set_char_size( size * 64, 0, 72*10, 72 )
        matrix = Matrix( int((0.1) * 0x10000L), int((0.0) * 0x10000L),
                         int((0.0) * 0x10000L), int((1.0) * 0x10000L) )
        previous = 0
        for current in text:
            face.set_transform( matrix, pen )
            face.load_char( current, FT_LOAD_RENDER
                                   | FT_LOAD_FORCE_AUTOHINT )
            kerning = face.get_kerning( previous, current, FT_KERNING_UNSCALED )
            glyph = face.glyph
            bitmap = glyph.bitmap
            pen.x += glyph.advance.x + kerning.x
            x, y = glyph.bitmap_left, glyph.bitmap_top
            w, h, p = bitmap.width, bitmap.rows, bitmap.pitch
            buff = np.array(bitmap.buffer, dtype=np.ubyte).reshape((h,p))
            Z[H-y:H-y+h,x:x+w].flat = buff[:,:w]
            previous = current
        pen.x  = 10*64
        pen.y -= (size+2)*64
        
    # Gamma correction
    Z = Z/255.0
    Z = Z**(1.75)
    Z = ((1-Z)*255).astype(np.ubyte)
    I = Image.fromarray(Z, mode='L')
    I.save('test.png')
