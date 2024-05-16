#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
from freetype import *

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: %s font_filename" % sys.argv[0])
        sys.exit()

    face = Face(sys.argv[1])

    print ('Family name:         {}'.format(face.family_name))
    print ('Style name:          {}'.format(face.style_name))
    print ('Charmaps:            {}'.format([charmap.encoding_name for charmap in face.charmaps]))
    print ('')
    print ('Face number:         {}'.format(face.num_faces))
    print ('Glyph number:        {}'.format(face.num_glyphs))
    # FT_Bitmap_Size.size is in F26.6. Need to divide by 64:
    print ('Available sizes:     {}'.format([bitmap_size.size/64 for bitmap_size in face.available_sizes]))
    print ('')
    print ('units per em:        {}'.format(face.units_per_EM))
    print ('ascender:            {}'.format(face.ascender))
    print ('descender:           {}'.format(face.descender))
    print ('height:              {}'.format(face.height))
    print ('')
    print ('max_advance_width:   {}'.format(face.max_advance_width))
    print ('max_advance_height:  {}'.format(face.max_advance_height))
    print ('')
    print ('underline_position:  {}'.format(face.underline_position))
    print ('underline_thickness: {}'.format(face.underline_thickness))
    print ('')
    print ('Has horizontal:      {}'.format(face.has_horizontal))
    print ('Has vertical:        {}'.format(face.has_vertical))
    print ('Has kerning:         {}'.format(face.has_kerning))
    print ('Is fixed width:      {}'.format(face.is_fixed_width))
    print ('Is scalable:         {}'.format(face.is_scalable))
    print ('')
