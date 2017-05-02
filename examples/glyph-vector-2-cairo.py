#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  pycairo/cairocffi-based glyph-vector-2 example - Copyright 2017 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  rewrite of the numply,matplotlib-based example from Nicolas P. Rougier
#  - The code is incomplete and over-simplified, as it ignores the 3rd order
#    bezier curve bit when intepolating between off-curve points.
#    This is only correct for truetype fonts (which only use 2nd order bezier curves).
#  - Also it seems to assume the first point is always on curve; this is
#    unusual but legal.
#
#  Can cope with well-behaved Postscript/CFF fonts too.
#
# -----------------------------------------------------------------------------
'''
Show how to access glyph outline description.
'''
from freetype import *
# using Matrix class from Cairo, instead of FreeType's
from cairo import Context, SVGSurface, Matrix, SurfacePattern, FILTER_BEST

from bitmap_to_surface import make_image_surface

if __name__ == '__main__':
    import numpy
    from PIL import Image

    # Replacement for Path enums:
    STOP, MOVETO, LINETO, CURVE3, CURVE4 = 0, 1, 2, 3, 4

    face = Face('./Vera.ttf')
    face.set_char_size( 32*64 )
    face.load_char('g')
    slot = face.glyph

    bitmap = face.glyph.bitmap
    width  = face.glyph.bitmap.width
    rows   = face.glyph.bitmap.rows
    pitch  = face.glyph.bitmap.pitch

    Z = make_image_surface(bitmap)

    outline = slot.outline
    points = numpy.array(outline.points, dtype=[('x',float), ('y',float)])
    x, y = points['x'], points['y']

    bbox = outline.get_bbox()

    MARGIN  = 10
    scale = 3

    width_s = ((bbox.xMax - bbox.xMin)//scale + 2 * MARGIN)
    height_s = ((bbox.yMax - bbox.yMin)//scale + 2 * MARGIN)

    surface = SVGSurface('glyph-vector-2-cairo.svg',
                         width_s,
                         height_s)
    ctx = Context(surface)
    ctx.set_source_rgb(1,1,1)
    ctx.paint()
    ctx.save()
    ctx.scale(1.0/scale,1.0/scale)
    ctx.translate(-bbox.xMin + MARGIN * scale,-bbox.yMin + MARGIN * scale)
    ctx.transform(Matrix(1,0,0,-1))
    ctx.translate(0, -(bbox.yMax + bbox.yMin)) # difference!

    start, end = 0, 0

    VERTS, CODES = [], []
    # Iterate over each contour
    for i in range(len(outline.contours)):
        end    = outline.contours[i]
        points = outline.points[start:end+1]
        points.append(points[0])
        tags   = outline.tags[start:end+1]
        tags.append(tags[0])

        segments = [ [points[0],], ]
        for j in range(1, len(points) ):
            segments[-1].append(points[j])
            if ( FT_Curve_Tag( tags[j] ) == FT_Curve_Tag_On ) and j < (len(points)-1):
                segments.append( [points[j],] )
        verts = [points[0], ]
        codes = [MOVETO,]
        tags.pop()
        for segment in segments:
            if len(segment) == 2:
                verts.extend(segment[1:])
                codes.extend([LINETO])
            elif len(segment) == 3:
                verts.extend(segment[1:])
                codes.extend([CURVE3, CURVE3])
            elif ( len(segment) == 4 ) \
                 and ( FT_Curve_Tag(tags[1]) == FT_Curve_Tag_Cubic ) \
                 and ( FT_Curve_Tag(tags[2]) == FT_Curve_Tag_Cubic ):
                verts.extend(segment[1:])
                codes.extend([CURVE4, CURVE4, CURVE4])
            else:
                # Interpolating
                verts.append(segment[1])
                codes.append(CURVE3)
                for i in range(1,len(segment)-2):
                    A,B = segment[i], segment[i+1]
                    C = ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0)
                    verts.extend([ C, B ])
                    codes.extend([ CURVE3, CURVE3])
                verts.append(segment[-1])
                codes.append(CURVE3)
            [tags.pop() for x in range(len(segment) - 1)]
        VERTS.extend(verts)
        CODES.extend(codes)
        start = end+1


    # Draw glyph
    ctx.new_path()
    ctx.set_source_rgba(0.8,0.5,0.8, 1)
    i = 0
    while (i < len(CODES)):
        if (CODES[i] == MOVETO):
            ctx.move_to(VERTS[i][0],VERTS[i][1])
            i += 1
        elif (CODES[i] == LINETO):
            ctx.line_to(VERTS[i][0],VERTS[i][1])
            i += 1
        elif (CODES[i] == CURVE3):
            ctx.curve_to(VERTS[i][0],VERTS[i][1],
                         VERTS[i+1][0],VERTS[i+1][1], # undocumented
                         VERTS[i+1][0],VERTS[i+1][1])
            i += 2
        elif (CODES[i] == CURVE4):
            ctx.curve_to(VERTS[i][0],VERTS[i][1],
                         VERTS[i+1][0],VERTS[i+1][1],
                         VERTS[i+2][0],VERTS[i+2][1])
            i += 3
    ctx.fill_preserve()
    ctx.set_source_rgb(0,0,0)
    ctx.set_line_width(6)
    ctx.stroke()
    ctx.restore()

    scale2 = (height_s - 2.0 * MARGIN)/rows

    ctx.set_source_surface(Z, 0, 0)
    pattern = ctx.get_source()
    SurfacePattern.set_filter(pattern, FILTER_BEST)
    scalematrix = Matrix()
    scalematrix.scale(1.0/scale2, 1.0/scale2)
    scalematrix.translate(-( width_s/2.0  - width *scale2 /2.0 ), -MARGIN)
    pattern.set_matrix(scalematrix)
    ctx.set_source_rgba (0, 0, 0, 0.7)
    ctx.mask(pattern)
    ctx.fill()


    surface.flush()
    surface.write_to_png("glyph-vector-2-cairo.png")
    surface.finish()
    Image.open("glyph-vector-2-cairo.png").show()
