# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
# -----------------------------------------------------------------------------
'''
Freetype raw API

This is the raw ctypes freetype binding.
'''
import sys,os,glob
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

def win_find_library(name):
        if name in ('c', 'm'):
            return find_msvcrt()
        # See MSDN for the REAL search order.
        for directory in os.environ['PATH'].split(os.pathsep):
            #fname = os.path.join(directory, name)
            if name.endswith(".dll"):
                fname = glob.glob( os.path.sep.join((directory,'*%s'%name)))
            else:
                fname = glob.glob( os.path.sep.join((directory,'*%s*.dll'%name )))
                
            if len(fname):
                fname = fname[0]
                if os.path.isfile(fname):
                    return fname
            continue
        return ''

if platform.system() == 'Windows': # add CWD to the search path
    CWD = os.path.realpath('.')
    if CWD not in os.environ['PATH']:
        os.environ['PATH'] = os.pathsep.join((os.environ['PATH'],CWD))

# add local DLLS directory to the search path (last ditch fail-safe)
DLL_directory = os.path.sep.join((os.path.dirname(__file__), 'DLLS'))
os.environ['PATH'] = os.pathsep.join((os.environ['PATH'],DLL_directory))

if platform.system() == 'Windows':
    found = win_find_library('freetype')
else:
    found = ctypes.util.find_library('freetype')

if not found:
    raise RuntimeError('Freetype library not found')

filepath,filename = os.path.split(found)

try:
    lastcwd = os.getcwd()
    os.chdir(filepath) # this method succeeds LoadLibrary(os.path.join(filepath,filename)) fails.
    _lib = ctypes.cdll.LoadLibrary(filename)
    os.chdir(lastcwd)
except (OSError, TypeError):
    _lib = None
    raise RuntimeError('Freetype library dependences not installed')

FT_Init_FreeType       = _lib.FT_Init_FreeType
FT_Done_FreeType       = _lib.FT_Done_FreeType
FT_Library_Version     = _lib.FT_Library_Version

try:
    FT_Library_SetLcdFilter= _lib.FT_Library_SetLcdFilter
except AttributeError:
    def FT_Library_SetLcdFilter (*args, **kwargs):
        return 0
try:
    FT_Library_SetLcdFilterWeights = _lib.FT_Library_SetLcdFilterWeights
except AttributeError:
    pass

FT_New_Face            = _lib.FT_New_Face
FT_New_Memory_Face     = _lib.FT_New_Memory_Face
FT_Open_Face           = _lib.FT_Open_Face
FT_Attach_File         = _lib.FT_Attach_File
FT_Attach_Stream       = _lib.FT_Attach_Stream

try:
    FT_Reference_Face      = _lib.FT_Reference_Face
except AttributeError:
	pass

FT_Done_Face           = _lib.FT_Done_Face
FT_Done_Glyph          = _lib.FT_Done_Glyph
FT_Select_Size         = _lib.FT_Select_Size
FT_Request_Size        = _lib.FT_Request_Size
FT_Set_Char_Size       = _lib.FT_Set_Char_Size
FT_Set_Pixel_Sizes     = _lib.FT_Set_Pixel_Sizes
FT_Load_Glyph          = _lib.FT_Load_Glyph
FT_Load_Char           = _lib.FT_Load_Char
FT_Set_Transform       = _lib.FT_Set_Transform
FT_Render_Glyph        = _lib.FT_Render_Glyph
FT_Get_Kerning         = _lib.FT_Get_Kerning
FT_Get_Track_Kerning   = _lib.FT_Get_Track_Kerning
FT_Get_Glyph_Name      = _lib.FT_Get_Glyph_Name
FT_Get_Glyph           = _lib.FT_Get_Glyph

FT_Glyph_Get_CBox      = _lib.FT_Glyph_Get_CBox

FT_Get_Postscript_Name = _lib.FT_Get_Postscript_Name
FT_Get_Postscript_Name.restype = c_char_p
FT_Select_Charmap      = _lib.FT_Select_Charmap
FT_Set_Charmap         = _lib.FT_Set_Charmap
FT_Get_Charmap_Index   = _lib.FT_Get_Charmap_Index
FT_Get_CMap_Language_ID= _lib.FT_Get_CMap_Language_ID
FT_Get_CMap_Format     = _lib.FT_Get_CMap_Format
FT_Get_Char_Index      = _lib.FT_Get_Char_Index
FT_Get_First_Char      = _lib.FT_Get_First_Char
FT_Get_Next_Char       = _lib.FT_Get_Next_Char
FT_Get_Name_Index      = _lib.FT_Get_Name_Index
FT_Get_SubGlyph_Info   = _lib.FT_Get_SubGlyph_Info

try:
    FT_Get_FSType_Flags    = _lib.FT_Get_FSType_Flags
    FT_Get_FSType_Flags.restype  = c_ushort
except AttributeError:
	pass

FT_Get_X11_Font_Format = _lib.FT_Get_X11_Font_Format
FT_Get_X11_Font_Format.restype = c_char_p

FT_Get_Sfnt_Name_Count = _lib.FT_Get_Sfnt_Name_Count
FT_Get_Sfnt_Name       = _lib.FT_Get_Sfnt_Name
try: FT_Get_Advance         = _lib.FT_Get_Advance
except: pass

FT_Outline_GetInsideBorder  = _lib.FT_Outline_GetInsideBorder
FT_Outline_GetOutsideBorder = _lib.FT_Outline_GetOutsideBorder
FT_Outline_Get_BBox         = _lib.FT_Outline_Get_BBox
FT_Outline_Get_CBox         = _lib.FT_Outline_Get_CBox
FT_Stroker_New              = _lib.FT_Stroker_New
FT_Stroker_Set              = _lib.FT_Stroker_Set
FT_Stroker_Rewind           = _lib.FT_Stroker_Rewind
FT_Stroker_ParseOutline     = _lib.FT_Stroker_ParseOutline
FT_Stroker_BeginSubPath     = _lib.FT_Stroker_BeginSubPath
FT_Stroker_EndSubPath       = _lib.FT_Stroker_EndSubPath
FT_Stroker_LineTo           = _lib.FT_Stroker_LineTo
FT_Stroker_ConicTo          = _lib.FT_Stroker_ConicTo
FT_Stroker_CubicTo          = _lib.FT_Stroker_CubicTo
FT_Stroker_GetBorderCounts  = _lib.FT_Stroker_GetBorderCounts
FT_Stroker_ExportBorder     = _lib.FT_Stroker_ExportBorder
FT_Stroker_GetCounts        = _lib.FT_Stroker_GetCounts
FT_Stroker_Export           = _lib.FT_Stroker_Export
FT_Stroker_Done             = _lib.FT_Stroker_Done
FT_Glyph_Stroke             = _lib.FT_Glyph_Stroke
FT_Glyph_StrokeBorder       = _lib.FT_Glyph_StrokeBorder
FT_Glyph_To_Bitmap          = _lib.FT_Glyph_To_Bitmap
