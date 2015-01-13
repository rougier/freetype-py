# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011-2014 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
'''
Freetype raw API

This is the raw ctypes freetype binding.
'''
import os
import platform
from ctypes import *
import ctypes.util

from freetype.ft_types import *
from freetype.ft_enums import *
from freetype.ft_errors import *
from freetype.ft_structs import *

__dll__    = None

# on windows all ctypes does when checking for the library
# is to append .dll to the end and look for an exact match
# within any entry in PATH.
filename = ctypes.util.find_library('freetype')

if filename is None:
    if platform.system() == 'Windows':
        # Check current working directory for dll as ctypes fails to do so
        filename = os.path.join(os.path.realpath('.'), 'freetype.dll')
    else:
        filename = 'libfreetype.so.6'

try:
    dll = ctypes.CDLL(filename)
    _found = True
except (OSError, TypeError):
    _found = False

if not _found:
    raise RuntimeError('Freetype library not found')

__dll__ = dll

FT_Init_FreeType       = __dll__.FT_Init_FreeType
FT_Done_FreeType       = __dll__.FT_Done_FreeType
FT_Library_Version     = __dll__.FT_Library_Version

try:
    FT_Library_SetLcdFilter= __dll__.FT_Library_SetLcdFilter
except AttributeError:
    def FT_Library_SetLcdFilter (*args, **kwargs):
        return 0
try:
    FT_Library_SetLcdFilterWeights = __dll__.FT_Library_SetLcdFilterWeights
except AttributeError:
    pass

FT_New_Face            = __dll__.FT_New_Face
FT_New_Memory_Face     = __dll__.FT_New_Memory_Face
FT_Open_Face           = __dll__.FT_Open_Face
FT_Attach_File         = __dll__.FT_Attach_File
FT_Attach_Stream       = __dll__.FT_Attach_Stream

try:
    FT_Reference_Face      = __dll__.FT_Reference_Face
except AttributeError:
	pass

FT_Done_Face           = __dll__.FT_Done_Face
FT_Done_Glyph          = __dll__.FT_Done_Glyph
FT_Select_Size         = __dll__.FT_Select_Size
FT_Request_Size        = __dll__.FT_Request_Size
FT_Set_Char_Size       = __dll__.FT_Set_Char_Size
FT_Set_Pixel_Sizes     = __dll__.FT_Set_Pixel_Sizes
FT_Load_Glyph          = __dll__.FT_Load_Glyph
FT_Load_Char           = __dll__.FT_Load_Char
FT_Set_Transform       = __dll__.FT_Set_Transform
FT_Render_Glyph        = __dll__.FT_Render_Glyph
FT_Get_Kerning         = __dll__.FT_Get_Kerning
FT_Get_Track_Kerning   = __dll__.FT_Get_Track_Kerning
FT_Get_Glyph_Name      = __dll__.FT_Get_Glyph_Name
FT_Get_Glyph           = __dll__.FT_Get_Glyph

FT_Glyph_Get_CBox      = __dll__.FT_Glyph_Get_CBox

FT_Get_Postscript_Name = __dll__.FT_Get_Postscript_Name
FT_Get_Postscript_Name.restype = c_char_p
FT_Select_Charmap      = __dll__.FT_Select_Charmap
FT_Set_Charmap         = __dll__.FT_Set_Charmap
FT_Get_Charmap_Index   = __dll__.FT_Get_Charmap_Index
FT_Get_CMap_Language_ID= __dll__.FT_Get_CMap_Language_ID
FT_Get_CMap_Format     = __dll__.FT_Get_CMap_Format
FT_Get_Char_Index      = __dll__.FT_Get_Char_Index
FT_Get_First_Char      = __dll__.FT_Get_First_Char
FT_Get_Next_Char       = __dll__.FT_Get_Next_Char
FT_Get_Name_Index      = __dll__.FT_Get_Name_Index
FT_Get_SubGlyph_Info   = __dll__.FT_Get_SubGlyph_Info

try:
    FT_Get_FSType_Flags    = __dll__.FT_Get_FSType_Flags
    FT_Get_FSType_Flags.restype  = c_ushort
except AttributeError:
	pass

FT_Get_X11_Font_Format = __dll__.FT_Get_X11_Font_Format
FT_Get_X11_Font_Format.restype = c_char_p

FT_Get_Sfnt_Name_Count = __dll__.FT_Get_Sfnt_Name_Count
FT_Get_Sfnt_Name       = __dll__.FT_Get_Sfnt_Name
FT_Get_Advance         = __dll__.FT_Get_Advance


FT_Outline_GetInsideBorder  = __dll__.FT_Outline_GetInsideBorder
FT_Outline_GetOutsideBorder = __dll__.FT_Outline_GetOutsideBorder
FT_Outline_Get_BBox         = __dll__.FT_Outline_Get_BBox
FT_Outline_Get_CBox         = __dll__.FT_Outline_Get_CBox
FT_Stroker_New              = __dll__.FT_Stroker_New
FT_Stroker_Set              = __dll__.FT_Stroker_Set
FT_Stroker_Rewind           = __dll__.FT_Stroker_Rewind
FT_Stroker_ParseOutline     = __dll__.FT_Stroker_ParseOutline
FT_Stroker_BeginSubPath     = __dll__.FT_Stroker_BeginSubPath
FT_Stroker_EndSubPath       = __dll__.FT_Stroker_EndSubPath
FT_Stroker_LineTo           = __dll__.FT_Stroker_LineTo
FT_Stroker_ConicTo          = __dll__.FT_Stroker_ConicTo
FT_Stroker_CubicTo          = __dll__.FT_Stroker_CubicTo
FT_Stroker_GetBorderCounts  = __dll__.FT_Stroker_GetBorderCounts
FT_Stroker_ExportBorder     = __dll__.FT_Stroker_ExportBorder
FT_Stroker_GetCounts        = __dll__.FT_Stroker_GetCounts
FT_Stroker_Export           = __dll__.FT_Stroker_Export
FT_Stroker_Done             = __dll__.FT_Stroker_Done
FT_Glyph_Stroke             = __dll__.FT_Glyph_Stroke
FT_Glyph_StrokeBorder       = __dll__.FT_Glyph_StrokeBorder
FT_Glyph_To_Bitmap          = __dll__.FT_Glyph_To_Bitmap