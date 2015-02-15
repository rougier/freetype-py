# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  FreeType high-level python API - Copyright 2011-2015 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
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

osName = platform.system()

if filename is None:
    if osName == 'Windows':
        # Check current working directory for dll as ctypes fails to do so
        filename = os.path.join(os.path.realpath('.'), 'freetype.dll')
    else:
        filename = 'libfreetype.so.6'

try:
    _lib = ctypes.CDLL(filename)
except (OSError, TypeError):
    _lib = None
    raise RuntimeError('Freetype library not found')


if osName == 'Windows':
    _funcType = WINFUNCTYPE
else: # Linux and OS X
    _funcType = CFUNCTYPE

def _def_func(name, returnType, paramTypes):
    '''Define function for library'''
    try:
        address = getattr(_lib, name)
        function = _funcType(returnType, *paramTypes)
    except AttributeError:
        raise AttributeError('{}: Function not found.'.format(name))
    return cast(address, function)


####### Functions/Macros ######

##### FT_CONFIG_CONFIG_H #####
##### FT_CONFIG_STANDARD_LIBRARY_H #####
##### FT_CONFIG_OPTIONS_H #####
##### FT_CONFIG_MODULES_H #####

##### FT_FREETYPE_H #####
#macros
# FT_ENC_TAG
# FT_HAS_HORIZONTAL
# FT_HAS_VERTICAL
# FT_HAS_KERNING
# FT_IS_SCALABLE
# FT_IS_SFNT
# FT_IS_FIXED_WIDTH
# FT_HAS_FIXED_SIZES
# FT_HAS_FAST_GLYPHS
# FT_HAS_GLYPH_NAMES
# FT_HAS_MULTIPLE_MASTERS
# FT_IS_CID_KEYED
# FT_IS_TRICKY
# FT_HAS_COLOR
#end macros
FT_Init_FreeType       = _def_func('FT_Init_FreeType', FT_Error, (POINTER(FT_Library),))
FT_Done_FreeType       = _def_func('FT_Done_FreeType', FT_Error, (FT_Library,))
FT_New_Face            = _def_func('FT_New_Face', FT_Error, (FT_Library, c_char_p, FT_Long, POINTER(FT_Face)))
FT_New_Memory_Face     = _def_func('FT_New_Memory_Face', FT_Error, (FT_Library, POINTER(FT_Byte), FT_Long, FT_Long, POINTER(FT_Face)))
FT_Open_Face           = _def_func('FT_Open_Face', FT_Error, (FT_Library, POINTER(FT_Open_Args), FT_Long, POINTER(FT_Face)))
FT_Attach_File         = _def_func('FT_Attach_File', FT_Error, (FT_Face, c_char_p))
FT_Attach_Stream       = _def_func('FT_Attach_Stream', FT_Error, (FT_Face, POINTER(FT_Open_Args)))
FT_Reference_Face      = _def_func('FT_Reference_Face', FT_Error, (FT_Face,)) # 2.4.2+
FT_Done_Face           = _def_func('FT_Done_Face', FT_Error, (FT_Face,))
FT_Select_Size         = _def_func('FT_Select_Size', FT_Error, (FT_Face, FT_Int))
FT_Request_Size        = _def_func('FT_Request_Size', FT_Error, (FT_Face, FT_Size_Request))
FT_Set_Char_Size       = _def_func('FT_Set_Char_Size', FT_Error, (FT_Face, FT_F26Dot6, FT_F26Dot6, FT_UInt, FT_UInt))
FT_Set_Pixel_Sizes     = _def_func('FT_Set_Pixel_Sizes', FT_Error, (FT_Face, FT_UInt, FT_UInt))
FT_Load_Glyph          = _def_func('FT_Load_Glyph', FT_Error, (FT_Face, FT_UInt, FT_Int32))
FT_Load_Char           = _def_func('FT_Load_Char', FT_Error, (FT_Face, FT_ULong, FT_Int32))
FT_Set_Transform       = _def_func('FT_Set_Transform', None, (FT_Face, POINTER(FT_Matrix), POINTER(FT_Vector)))
FT_Render_Glyph        = _def_func('FT_Render_Glyph', FT_Error, (FT_GlyphSlot, FT_Render_Mode))
FT_Get_Kerning         = _def_func('FT_Get_Kerning', FT_Error, (FT_Face, FT_UInt, FT_UInt, FT_UInt, POINTER(FT_Vector)))
FT_Get_Track_Kerning   = _def_func('FT_Get_Track_Kerning', FT_Error, (FT_Face, FT_Fixed, FT_Int, POINTER(FT_Fixed)))
FT_Get_Glyph_Name      = _def_func('FT_Get_Glyph_Name', FT_Error, (FT_Face, FT_UInt, FT_Pointer, FT_UInt))
FT_Get_Postscript_Name = _def_func('FT_Get_Postscript_Name', c_char_p, (FT_Face,))
FT_Select_Charmap      = _def_func('FT_Select_Charmap', FT_Error, (FT_Face, FT_Encoding))
FT_Set_Charmap         = _def_func('FT_Set_Charmap', FT_Error, (FT_Face, FT_CharMap))
FT_Get_Charmap_Index   = _def_func('FT_Get_Charmap_Index', FT_Error, (FT_CharMap,))
FT_Get_Char_Index      = _def_func('FT_Get_Char_Index', FT_UInt, (FT_Face, FT_ULong))
FT_Get_First_Char      = _def_func('FT_Get_First_Char', FT_ULong, (FT_Face, FT_UInt))
FT_Get_Next_Char       = _def_func('FT_Get_Next_Char', FT_ULong, (FT_Face, FT_ULong, POINTER(FT_UInt)))
FT_Get_Name_Index      = _def_func('FT_Get_Name_Index', FT_UInt, (FT_Face, POINTER(FT_String)))
FT_Get_SubGlyph_Info   = _def_func('FT_Get_SubGlyph_Info', FT_Error, (FT_GlyphSlot, FT_UInt, POINTER(FT_Int), POINTER(FT_UInt), POINTER(FT_Int), POINTER(FT_Int), POINTER(FT_Matrix)))
FT_Get_FSType_Flags    = _def_func('FT_Get_FSType_Flags', FT_UShort, (FT_Face,)) # 2.3.8+
# FT_Face_GetCharVariantIndex # 2.3.6+
# FT_Face_GetCharVariantIsDefault # 2.3.6+
# FT_Face_GetVariantSelectors # 2.3.6+
# FT_Face_GetVariantsOfChar # 2.3.6+
# FT_Face_GetCharsOfVariant # 2.3.6+
# FT_MulDiv
# FT_MulFix
# FT_DivFix
# FT_RoundFix
# FT_CeilFix
# FT_FloorFix
# FT_Vector_Transform
FT_Library_Version     = _def_func('FT_Library_Version', None, (FT_Library, POINTER(FT_Int), POINTER(FT_Int), POINTER(FT_Int)))
# FT_Face_CheckTrueTypePatents # 2.3.5+
# FT_Face_SetUnpatentedHinting # 2.3.5+

##### FT_ERRORS_H #####
##### FT_MODULE_ERRORS_H #####
##### FT_SYSTEM_H #####
##### FT_IMAGE_H #####
##### FT_TYPES_H #####
##### FT_LIST_H #####

##### FT_OUTLINE_H #####
# FT_Outline_Decompose
# FT_Outline_New
# FT_Outline_New_Internal
# FT_Outline_Done
# FT_Outline_Done_Internal
# FT_Outline_Check
FT_Outline_Get_CBox         = _def_func('FT_Outline_Get_CBox', POINTER(FT_Outline), (POINTER(FT_BBox),))
# FT_Outline_Translate
# FT_Outline_Copy
# FT_Outline_Transform
# FT_Outline_Embolden
# FT_Outline_EmboldenXY
# FT_Outline_Reverse
# FT_Outline_Get_Bitmap
# FT_Outline_Render
# FT_Outline_Get_Orientation

##### FT_SIZES_H #####
##### FT_MODULE_H #####
##### FT_RENDER_H #####
##### FT_AUTOHINTER_H #####
##### FT_CFF_DRIVER_H #####
##### FT_TRUETYPE_DRIVER_H #####
##### FT_TYPE1_TABLES_H #####
##### FT_TRUETYPE_IDS_H #####

##### FT_TRUETYPE_TABLES_H #####
# FT_Get_Sfnt_Table
# FT_Load_Sfnt_Table
# FT_Sfnt_Table_Info
FT_Get_CMap_Language_ID= _def_func('FT_Get_CMap_Language_ID', FT_ULong, (FT_CharMap,))
FT_Get_CMap_Format     = _def_func('FT_Get_CMap_Format', FT_Long, (FT_CharMap,))

##### FT_TRUETYPE_TAGS_H #####
##### FT_BDF_H #####
##### FT_CID_H #####
##### FT_GZIP_H #####
##### FT_LZW_H #####
##### FT_BZIP2_H #####
##### FT_WINFONTS_H #####

##### FT_GLYPH_H #####
FT_Get_Glyph           = _def_func('FT_Get_Glyph', FT_Error, (FT_GlyphSlot, POINTER(FT_Glyph)))
# FT_Glyph_Copy
# FT_Glyph_Transform
FT_Glyph_Get_CBox      = _def_func('FT_Glyph_Get_CBox', None, (FT_Glyph, FT_UInt, POINTER(FT_BBox)))
FT_Glyph_To_Bitmap     = _def_func('FT_Glyph_To_Bitmap', FT_Error, (POINTER(FT_Glyph), FT_Render_Mode, POINTER(FT_Vector), FT_Bool))
FT_Done_Glyph          = _def_func('FT_Done_Glyph', None, (FT_Glyph,))
# FT_Matrix_Multiply
# FT_Matrix_Invert

##### FT_BITMAP_H #####

##### FT_BBOX_H #####
FT_Outline_Get_BBox         = _def_func('FT_Outline_Get_BBox', FT_Error, (POINTER(FT_Outline), POINTER(FT_BBox)))

##### FT_CACHE_H #####
##### FT_MAC_H #####
##### FT_MULTIPLE_MASTERS_H #####

##### FT_SFNT_NAMES_H #####
FT_Get_Sfnt_Name_Count = _def_func('FT_Get_Sfnt_Name_Count', FT_UInt, (FT_Face,))
FT_Get_Sfnt_Name       = _def_func('FT_Get_Sfnt_Name', FT_UInt, (FT_Face, FT_UInt, POINTER(FT_SfntName)))

##### FT_OPENTYPE_VALIDATE_H #####
##### FT_GX_VALIDATE_H #####
##### FT_PFR_H #####

##### FT_STROKER_H #####
FT_Outline_GetInsideBorder  = _def_func('FT_Outline_GetInsideBorder', FT_StrokerBorder, (POINTER(FT_Outline),))
FT_Outline_GetOutsideBorder = _def_func('FT_Outline_GetOutsideBorder', FT_StrokerBorder, (POINTER(FT_Outline),))
FT_Stroker_New              = _def_func('FT_Stroker_New', FT_Error, (FT_Library, POINTER(FT_Stroker)))
FT_Stroker_Set              = _def_func('FT_Stroker_Set', None, (FT_Stroker, FT_Fixed, FT_Stroker_LineCap, FT_Stroker_LineJoin, FT_Fixed))
FT_Stroker_Rewind           = _def_func('FT_Stroker_Rewind', None, (FT_Stroker,) )
FT_Stroker_ParseOutline     = _def_func('FT_Stroker_ParseOutline', FT_Error, (FT_Stroker, POINTER(FT_Outline), FT_Bool))
FT_Stroker_BeginSubPath     = _def_func('FT_Stroker_BeginSubPath', FT_Error, (FT_Stroker, POINTER(FT_Vector), FT_Bool))
FT_Stroker_EndSubPath       = _def_func('FT_Stroker_EndSubPath', FT_Error, (FT_Stroker,))
FT_Stroker_LineTo           = _def_func('FT_Stroker_LineTo', FT_Error, (FT_Stroker, POINTER(FT_Vector)))
FT_Stroker_ConicTo          = _def_func('FT_Stroker_ConicTo', FT_Error, (FT_Stroker, POINTER(FT_Vector), POINTER(FT_Vector)))
FT_Stroker_CubicTo          = _def_func('FT_Stroker_CubicTo', FT_Error, (FT_Stroker, POINTER(FT_Vector), POINTER(FT_Vector), POINTER(FT_Vector)))
FT_Stroker_GetBorderCounts  = _def_func('FT_Stroker_GetBorderCounts', FT_Error, (FT_Stroker, FT_StrokerBorder, POINTER(FT_UInt), POINTER(FT_UInt)))
FT_Stroker_ExportBorder     = _def_func('FT_Stroker_ExportBorder', None, (FT_Stroker, FT_StrokerBorder, POINTER(FT_Outline)))
FT_Stroker_GetCounts        = _def_func('FT_Stroker_GetCounts', FT_Error, (FT_Stroker, POINTER(FT_UInt), POINTER(FT_UInt)))
FT_Stroker_Export           = _def_func('FT_Stroker_Export', None, (FT_Stroker, POINTER(FT_Outline)))
FT_Stroker_Done             = _def_func('FT_Stroker_Done', None, (FT_Stroker,))
FT_Glyph_Stroke             = _def_func('FT_Glyph_Stroke', FT_Error, (POINTER(FT_Glyph), FT_Stroker, FT_Bool))
FT_Glyph_StrokeBorder       = _def_func('FT_Glyph_StrokeBorder', FT_Error, (POINTER(FT_Glyph), FT_Stroker, FT_Bool, FT_Bool))

##### FT_SYNTHESIS_H #####

##### FT_XFREE86_H #####
FT_Get_X11_Font_Format = _def_func('FT_Get_X11_Font_Format', c_char_p, (FT_Face,))

##### FT_TRIGONOMETRY_H #####

##### FT_LCD_FILTER_H #####
FT_Library_SetLcdFilter        = _def_func('FT_Library_SetLcdFilter', FT_Error, (FT_Library, FT_LcdFilter)) # 2.3.0+
FT_Library_SetLcdFilterWeights = _def_func('FT_Library_SetLcdFilterWeights', FT_Error, (FT_Library, POINTER(c_ubyte))) # 2.4.0+

##### FT_UNPATENTED_HINTING_H #####
##### FT_INCREMENTAL_H #####
##### FT_GASP_H #####

##### FT_ADVANCES_H #####
FT_Get_Advance     = _def_func('FT_Get_Advance', FT_Error, (FT_Face, FT_UInt, FT_Int32, POINTER(FT_Fixed)))
# FT_Get_Advances

##### FT_ERROR_DEFINITIONS_H #####
##### FT_INCREMENTAL_H #####
##### FT_TRUETYPE_UNPATENTED_H #####
