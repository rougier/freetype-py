#!/usr/bin/env python
##
## This script shows how to retrieve and transform the contours
## for display without depending on third-party libraries to
## handle the bezier transformation.  The output is compatible
## with OpenSCAD's Polygon() primitive.
##
## Author: Giles Hall, July 2014
##

from freetype import *
import pprint
import operator
import fractions

SET_FLAG = (1 << 0)
DROPOUT_FLAG = (1 << 2)
DROPOUT_MASK = (1 << 5) | (1 << 6) | (1 << 7)

def binomial(n, k): 
    # http://stackoverflow.com/questions/3025162/statistics-combinations-in-python
    return int(reduce(operator.mul, (fractions.Fraction(n-i, i+1) for i in xrange(k)), 1))

def bezier_curve(points, steps):
    # http://pomax.github.io/bezierinfo/
    npts = len(points) - 1
    ndims = len(points[0])
    _points = [[pt[dim] for pt in points] for dim in xrange(ndims)]
    def intp(t, n, i, pt):
        polyt = ((1 - t) ** (n - i)) * (t ** i)
        return binomial(n, i) * polyt * pt
    for step in xrange(steps + 1):
        step = float(step) / steps
        yield tuple([sum([intp(step, npts, pidx, pt) for (pidx, pt) in enumerate(dim)]) for dim in _points])

def midpoint(pt1, pt2):
    res = []
    for (p1, p2) in zip(pt1, pt2):
        res.append((p1 + p2) / 2.0)
    return tuple(res)

# Iterate over each contour
def process_contours(outline):
    contours = []
    start = 0
    for contour in outline.contours:
        lastcp = None
        end = contour + 1
        content = zip(outline.tags[start:end], outline.points[start:end])
        start = end
        contour = []
        content.reverse()
    
        while content:
            (tag, point) = content.pop()
            if (tag & SET_FLAG):
                if lastcp:
                    contour[-1].extend([point])
                contour.append([point])
                lastcp = None
            else:
                if lastcp:
                    mp = midpoint(lastcp, point)
                    contour[-1].extend([mp])
                    contour.append([mp])
                contour[-1].extend([point])
                lastcp = point
            if (tag & DROPOUT_FLAG):
                dropout = DROPOUT_MASK & tag
        contour[-1].append(contour[0][0])
        contours.append(contour)
    return contours

def outline_font(outline, steps=10):
    points = []
    paths = []
    cnt = 0
    contours = process_contours(outline)
    for contour in contours:
        path = []
        for segment in contour:
            cnt = len(points)
            if len(segment) <= 2:
                points.extend(segment)
                path.append(cnt)
            else:
                curve = list(bezier_curve(segment, steps))
                path.extend(range(cnt, cnt + len(curve)))
                points.extend(curve)
        paths.append(path)
    return {"points": points, "paths": paths}

if __name__ == "__main__":
    face = Face('./Vera.ttf')
    face.set_char_size(48*64)
    face.load_char('S')
    slot = face.glyph
    outline = slot.outline
    args = outline_font(outline)
    pprint.pprint(args)
