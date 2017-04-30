#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  pycairo/cairocffi-based glyph-vector example - Copyright 2017 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.
#
#  rewrite of the numply,matplotlib-based example from Nicolas P. Rougier
#  - The code is strickly speaking not optimal, as it ignores the 3rd order
#    bezier curve bit and always intepolate between off-curve points.
#    This is only correct for truetype fonts (which only use 2nd order bezier curves).
#  - Also it seems to assume the first point is always on curve; this is
#    unusual but legal.
#
# -----------------------------------------------------------------------------
'''
Show how to access glyph outline description.
'''
from freetype import *

# using Matrix class from Cairo, instead of FreeType's
from cairo import Context, ImageSurface, FORMAT_ARGB32, Matrix

# use math.pi for drawing circles
import math

if __name__ == '__main__':
    import numpy
    from PIL import Image

    # Replacement for Path enums:
    STOP, MOVETO, LINETO, CURVE3, CURVE4 = 0, 1, 2, 3, 4

    def tag_meaning(tag):
        # return on/off_curve(), is_3rd_order_control_point()
        return [tag & 1 == 1, tag & 2 == 2]

    face = Face('./Vera.ttf')
    face.set_char_size( 48*64 )
    face.load_char('S')
    slot = face.glyph

    outline = slot.outline
    points = numpy.array(outline.points, dtype=[('x',float), ('y',float)])
    x, y = points['x'], points['y']

    cbox = outline.get_cbox()
    surface = ImageSurface(FORMAT_ARGB32,
                           (cbox.xMax - cbox.xMin)//4 + 20,
                           (cbox.yMax - cbox.yMin)//4 + 20)
    ctx = Context(surface)
    ctx.scale(0.25,0.25)
    ctx.translate(-cbox.xMin + 40,-cbox.yMin + 40)
    ctx.transform(Matrix(1,0,0,-1))
    ctx.translate(0, -(cbox.yMax + cbox.yMin)) # difference!

    meaning = [tag_meaning(tag) for tag in outline.tags]

    start, end = 0, 0

    VERTS, CODES = [], []
    # Iterate over each contour
    ctx.set_source_rgb(0.5,0.5,0.5)
    for i in range(len(outline.contours)):
        end    = outline.contours[i]

        ctx.move_to(outline.points[start][0],outline.points[start][1])
        for j in range(start, end+1):
            point = outline.points[j]
            ctx.line_to(point[0],point[1])
        #back to origin
        ctx.line_to(outline.points[start][0], outline.points[start][1])
        start = end+1
    ctx.fill_preserve()
    ctx.set_source_rgb(0,1,0)
    ctx.stroke()

    start, end = 0, 0
    for i in range(len(outline.contours)):
        end    = outline.contours[i]

        ctx.new_path()
        ctx.set_source_rgb(0,0,1)
        for j in range(start, end+1):
            if ( meaning[j][0] ):
                point = outline.points[j]
                ctx.move_to(point[0],point[1])
                ctx.arc(point[0], point[1], 40, 0, 2 * math.pi)
        ctx.fill()

        ctx.new_path()
        ctx.set_source_rgb(1,0,0)
        for j in range(start, end+1):
            if ( not meaning[j][0] ):
                point = outline.points[j]
                ctx.move_to(point[0],point[1])
                ctx.arc(point[0], point[1], 10, 0, 2 * math.pi)
        ctx.fill()

        points = outline.points[start:end+1]
        points.append(points[0])
        tags   = outline.tags[start:end+1]
        tags.append(tags[0])

        segments = [ [points[0],], ]
        for j in range(1, len(points) ):
            segments[-1].append(points[j])
            if tags[j] & (1 << 0) and j < (len(points)-1):
                segments.append( [points[j],] )
        verts = [points[0], ]
        codes = [MOVETO,]
        for segment in segments:
            if len(segment) == 2:
                verts.extend(segment[1:])
                codes.extend([LINETO])
            elif len(segment) == 3:
                verts.extend(segment[1:])
                codes.extend([CURVE3, CURVE3])
            else:
                verts.append(segment[1])
                codes.append(CURVE3)
                for i in range(1,len(segment)-2):
                    A,B = segment[i], segment[i+1]
                    C = ((A[0]+B[0])/2.0, (A[1]+B[1])/2.0)
                    verts.extend([ C, B ])
                    codes.extend([ CURVE3, CURVE3])
                verts.append(segment[-1])
                codes.append(CURVE3)
        VERTS.extend(verts)
        CODES.extend(codes)
        start = end+1

    ctx.new_path()
    ctx.set_source_rgba(1,1,0, 0.5)
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
        else:
            raise NotImplementedError("Cannot cope!")
    ctx.fill()

    surface.flush()
    surface.write_to_png("glyph-vector-cairo.png")
    Image.open("glyph-vector-cairo.png").show()
