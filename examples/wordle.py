# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
import math
import numpy as np
from freetype import *
import matplotlib.pyplot as plt


def make_label(text, filename, size=12, angle=0):
    '''
    Parameters:
    -----------
    text : string
        Text to be displayed
    filename : string
        Path to a font
    size : int
        Font size in 1/64th points
    angle : float
        Text angle in degrees
    '''
    face = Face(filename)
    face.set_char_size( size*64 )
    angle = (angle/180.0)*math.pi
    matrix  = FT_Matrix( (int)( math.cos( angle ) * 0x10000L ),
                         (int)(-math.sin( angle ) * 0x10000L ),
                         (int)( math.sin( angle ) * 0x10000L ),
                         (int)( math.cos( angle ) * 0x10000L ))
    flags = FT_LOAD_RENDER
    pen = FT_Vector(0,0)
    FT_Set_Transform( face._FT_Face, byref(matrix), byref(pen) )
    previous = 0
    xmin, xmax = 0, 0
    ymin, ymax = 0, 0
    for c in text:
        face.load_char(c, flags)
        kerning = face.get_kerning(previous, c)
        previous = c
        bitmap = face.glyph.bitmap
        pitch  = face.glyph.bitmap.pitch
        width  = face.glyph.bitmap.width
        rows   = face.glyph.bitmap.rows
        top    = face.glyph.bitmap_top
        left   = face.glyph.bitmap_left
        pen.x += kerning.x
        x0 = (pen.x >> 6) + left
        x1 = x0 + width
        y0 = (pen.y >> 6) - (rows - top)
        y1 = y0 + rows
        xmin, xmax = min(xmin, x0),  max(xmax, x1)
        ymin, ymax = min(ymin, y0), max(ymax, y1)
        pen.x += face.glyph.advance.x
        pen.y += face.glyph.advance.y

    L = np.zeros((ymax-ymin, xmax-xmin),dtype=np.ubyte)
    previous = 0
    pen.x, pen.y = 0, 0
    for c in text:
        face.load_char(c, flags)
        kerning = face.get_kerning(previous, c)
        previous = c
        bitmap = face.glyph.bitmap
        pitch  = face.glyph.bitmap.pitch
        width  = face.glyph.bitmap.width
        rows   = face.glyph.bitmap.rows
        top    = face.glyph.bitmap_top
        left   = face.glyph.bitmap_left
        pen.x += kerning.x
        x = (pen.x >> 6) - xmin + left
        y = (pen.y >> 6) - ymin - (rows - top)
        data = []
        for j in range(rows):
            data.extend(bitmap.buffer[j*pitch:j*pitch+width])
        if len(data):
            Z = np.array(data,dtype=np.ubyte).reshape(rows, width)
            L[y:y+rows,x:x+width] |= Z[::-1,::1]
        pen.x += face.glyph.advance.x
        pen.y += face.glyph.advance.y

    return L


if __name__ == '__main__':
    import Image

    n_words = 100
    n_tries = 100
    H, W = 600, 800

    I = np.zeros((H, W, 3), dtype=np.ubyte)
    S = np.random.normal(0,1,n_words)
    S = (S-S.min())/(S.max()-S.min())
    S = np.sort(1-np.sqrt(S))[::-1]
    sizes = (12 + S*96).astype(int).tolist()

    fails = 0
    for size in sizes:
        angle = np.random.randint(-25,25)
        L = make_label('Hello', './Vera.ttf', size, angle=angle)
        h,w = L.shape
        if h < H and w < W:
            for i in range(n_tries):
                c = .25+.75*np.random.random()
                x = np.random.randint(0,W-w)
                y = np.random.randint(0,H-h)
                if (I[y:y+h,x:x+w,0] * L).sum() == 0:
                    I[y:y+h,x:x+w,0] |= (c * L).astype(int)
                    I[y:y+h,x:x+w,1] |= (c * L).astype(int)
                    I[y:y+h,x:x+w,2] |= (c * L).astype(int)
                    break
            if i == n_tries:
                fails += 1

    print "Number of fails:", fails
    plt.imshow(I, interpolation='nearest', cmap=plt.cm.gray, origin='lower')
    plt.show()
    I = Image.fromarray(I, mode='RGB')
    I.save('wordle.png')

