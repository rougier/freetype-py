#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2018 Dean Serenevy <dean@serenevy.net>
# SPDX-License-Identifier: BSD-3-Clause-Clear
'''
Show how to use outline decompose.
'''
import os
import sys

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import freetype

def move_to(a, ctx):
    ctx.append("M {},{}".format(a.x, a.y))

def line_to(a, ctx):
    ctx.append("L {},{}".format(a.x, a.y))

def conic_to(a, b, ctx):
    ctx.append("Q {},{} {},{}".format(a.x, a.y, b.x, b.y))

def cubic_to(a, b, c, ctx):
    ctx.append("C {},{} {},{} {},{}".format(a.x, a.y, b.x, b.y, c.x, c.y))

if __name__ == '__main__':
    face = freetype.Face('./Vera.ttf')
    face.set_char_size( 18*64 )
    face.load_char('B', freetype.FT_LOAD_DEFAULT | freetype.FT_LOAD_NO_BITMAP)
    ctx = []
    face.glyph.outline.decompose(ctx, move_to=move_to, line_to=line_to, conic_to=conic_to, cubic_to=cubic_to)
    print("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg">
  <g>
    <path
      style="fill:none;stroke:#000000;stroke-width:2;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none;stroke-dashoffset:0"
      d="{}"
    />
  </g>
</svg>
""".format(" ".join(ctx)))
