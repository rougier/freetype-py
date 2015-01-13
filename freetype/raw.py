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
    _dll = ctypes.CDLL(filename)
except (OSError, TypeError):
    _dll = None
    raise RuntimeError('Freetype library not found')

FT_Init_FreeType       = _dll.FT_Init_FreeType
FT_Done_FreeType       = _dll.FT_Done_FreeType
FT_Library_Version     = _dll.FT_Library_Version

try:
    FT_Library_SetLcdFilter= _dll.FT_Library_SetLcdFilter
except AttributeError:
    def FT_Library_SetLcdFilter (*args, **kwargs):
        return 0
try:
    FT_Library_SetLcdFilterWeights = _dll.FT_Library_SetLcdFilterWeights
except AttributeError:
    pass

FT_New_Face            = _dll.FT_New_Face
FT_New_Memory_Face     = _dll.FT_New_Memory_Face
FT_Open_Face           = _dll.FT_Open_Face
FT_Attach_File         = _dll.FT_Attach_File
FT_Attach_Stream       = _dll.FT_Attach_Stream

try:
    FT_Reference_Face      = _dll.FT_Reference_Face
except AttributeError:
	pass

FT_Done_Face           = _dll.FT_Done_Face
FT_Done_Glyph          = _dll.FT_Done_Glyph
FT_Select_Size         = _dll.FT_Select_Size
FT_Request_Size        = _dll.FT_Request_Size
FT_Set_Char_Size       = _dll.FT_Set_Char_Size
FT_Set_Pixel_Sizes     = _dll.FT_Set_Pixel_Sizes
FT_Load_Glyph          = _dll.FT_Load_Glyph
FT_Load_Char           = _dll.FT_Load_Char
FT_Set_Transform       = _dll.FT_Set_Transform
FT_Render_Glyph        = _dll.FT_Render_Glyph
FT_Get_Kerning         = _dll.FT_Get_Kerning
FT_Get_Track_Kerning   = _dll.FT_Get_Track_Kerning
FT_Get_Glyph_Name      = _dll.FT_Get_Glyph_Name
FT_Get_Glyph           = _dll.FT_Get_Glyph

FT_Glyph_Get_CBox      = _dll.FT_Glyph_Get_CBox

FT_Get_Postscript_Name = _dll.FT_Get_Postscript_Name
FT_Get_Postscript_Name.restype = c_char_p
FT_Select_Charmap      = _dll.FT_Select_Charmap
FT_Set_Charmap         = _dll.FT_Set_Charmap
FT_Get_Charmap_Index   = _dll.FT_Get_Charmap_Index
FT_Get_CMap_Language_ID= _dll.FT_Get_CMap_Language_ID
FT_Get_CMap_Format     = _dll.FT_Get_CMap_Format
FT_Get_Char_Index      = _dll.FT_Get_Char_Index
FT_Get_First_Char      = _dll.FT_Get_First_Char
FT_Get_Next_Char       = _dll.FT_Get_Next_Char
FT_Get_Name_Index      = _dll.FT_Get_Name_Index
FT_Get_SubGlyph_Info   = _dll.FT_Get_SubGlyph_Info

try:
    FT_Get_FSType_Flags    = _dll.FT_Get_FSType_Flags
    FT_Get_FSType_Flags.restype  = c_ushort
except AttributeError:
	pass

FT_Get_X11_Font_Format = _dll.FT_Get_X11_Font_Format
FT_Get_X11_Font_Format.restype = c_char_p

FT_Get_Sfnt_Name_Count = _dll.FT_Get_Sfnt_Name_Count
FT_Get_Sfnt_Name       = _dll.FT_Get_Sfnt_Name
FT_Get_Advance         = _dll.FT_Get_Advance


FT_Outline_GetInsideBorder  = _dll.FT_Outline_GetInsideBorder
FT_Outline_GetOutsideBorder = _dll.FT_Outline_GetOutsideBorder
FT_Outline_Get_BBox         = _dll.FT_Outline_Get_BBox
FT_Outline_Get_CBox         = _dll.FT_Outline_Get_CBox
FT_Stroker_New              = _dll.FT_Stroker_New
FT_Stroker_Set              = _dll.FT_Stroker_Set
FT_Stroker_Rewind           = _dll.FT_Stroker_Rewind
FT_Stroker_ParseOutline     = _dll.FT_Stroker_ParseOutline
FT_Stroker_BeginSubPath     = _dll.FT_Stroker_BeginSubPath
FT_Stroker_EndSubPath       = _dll.FT_Stroker_EndSubPath
FT_Stroker_LineTo           = _dll.FT_Stroker_LineTo
FT_Stroker_ConicTo          = _dll.FT_Stroker_ConicTo
FT_Stroker_CubicTo          = _dll.FT_Stroker_CubicTo
FT_Stroker_GetBorderCounts  = _dll.FT_Stroker_GetBorderCounts
FT_Stroker_ExportBorder     = _dll.FT_Stroker_ExportBorder
FT_Stroker_GetCounts        = _dll.FT_Stroker_GetCounts
FT_Stroker_Export           = _dll.FT_Stroker_Export
FT_Stroker_Done             = _dll.FT_Stroker_Done
FT_Glyph_Stroke             = _dll.FT_Glyph_Stroke
FT_Glyph_StrokeBorder       = _dll.FT_Glyph_StrokeBorder
FT_Glyph_To_Bitmap          = _dll.FT_Glyph_To_Bitmap