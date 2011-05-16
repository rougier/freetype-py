#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#
#  FreeType high-level python API - Copyright 2011 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
#
# -----------------------------------------------------------------------------
'''
Freetype enum types
-------------------

FT_PIXEL_MODES: An enumeration type used to describe the format of pixels in a
                given bitmap. Note that additional formats may be added in the
                future.

FT_GLYPH_BBOX_MODES: The mode how the values of FT_Glyph_Get_CBox are returned.

FT_GLYPH_FORMATS: An enumeration type used to describe the format of a given
                  glyph image. Note that this version of FreeType only supports
                  two image formats, even though future font drivers will be
                  able to register their own format.

FT_ENCODINGS: An enumeration used to specify character sets supported by
              charmaps. Used in the FT_Select_Charmap API function.

FT_RENDER_MODES: An enumeration type that lists the render modes supported by
                 FreeType 2. Each mode corresponds to a specific type of
                 scanline conversion performed on the outline.

FT_LOAD_TARGETS: A list of values that are used to select a specific hinting
                 algorithm to use by the hinter. You should OR one of these
                 values to your 'load_flags' when calling FT_Load_Glyph.

FT_LOAD_FLAGS: A list of bit-field constants used with FT_Load_Glyph to
               indicate what kind of operations to perform during glyph
               loading.

FT_STYLE_FLAGS: A list of bit-flags used to indicate the style of a given
                face. These are used in the 'style_flags' field of FT_FaceRec.

FT_FACE_FLAGS: A list of bit flags used in the 'face_flags' field of the
               FT_FaceRec structure. They inform client applications of
               properties of the corresponding face.

FT_OUTLINE_FLAGS: A list of bit-field constants use for the flags in an
                  outline's 'flags' field.

FT_OPEN_MODES: A list of bit-field constants used within the 'flags' field of
               the FT_Open_Args structure.

FT_KERNING_MODES: An enumeration used to specify which kerning values to return
                  in FT_Get_Kerning.

FT_STROKER_LINEJOINS: These values determine how two joining lines are rendered
                      in a stroker.

FT_STROKER_LINECAPS: These values determine how the end of opened sub-paths are
                     rendered in a stroke.

FT_STROKER_BORDERS: These values are used to select a given stroke border in
                    FT_Stroker_GetBorderCounts and FT_Stroker_ExportBorder.

FT_LCD_FILTERS: A list of values to identify various types of LCD filters.

TT_PLATFORMS: A list of valid values for the 'platform_id' identifier code in
              FT_CharMapRec and FT_SfntName structures.

TT_APPLE_IDS: A list of valid values for the 'encoding_id' for
              TT_PLATFORM_APPLE_UNICODE charmaps and name entries.
 
TT_MAC_IDS: A list of valid values for the 'encoding_id' for
            TT_PLATFORM_MACINTOSH charmaps and name entries.

TT_MS_IDS: A list of valid values for the 'encoding_id' for
           TT_PLATFORM_MICROSOFT charmaps and name entries.

TT_ADOBE_IDS: A list of valid values for the 'encoding_id' for
              TT_PLATFORM_ADOBE charmaps. This is a FreeType-specific
              extension!

TT_MAC_LANGIDS: Possible values of the language identifier field in the name
                records of the TTF `name' table if the `platform' identifier
                code is TT_PLATFORM_MACINTOSH.

TT_MS_LANGIDS: Possible values of the language identifier field in the name
               records of the TTF `name' table if the `platform' identifier
               code is TT_PLATFORM_MICROSOFT.

TT_NAME_IDS: Possible values of the `name' identifier field in the name
             records of the TTF `name' table.  These values are platform
             independent.
'''

# -----------------------------------------------------------------------------
# An enumeration type used to describe the format of pixels in a given
# bitmap. Note that additional formats may be added in the future.
#
# FT_PIXEL_MODE_NONE	
# Value 0 is reserved.
#
# FT_PIXEL_MODE_MONO	
# A monochrome bitmap, using 1 bit per pixel. Note that pixels are stored in
# most-significant order (MSB), which means that the left-most pixel in a byte
# has value 128.
#
# FT_PIXEL_MODE_GRAY	
# An 8-bit bitmap, generally used to represent anti-aliased glyph images. Each
# pixel is stored in one byte. Note that the number of 'gray' levels is stored
# in the 'num_grays' field of the FT_Bitmap structure (it generally is 256).
#
# FT_PIXEL_MODE_GRAY2	
# A 2-bit per pixel bitmap, used to represent embedded anti-aliased bitmaps in
# font files according to the OpenType specification. We haven't found a single
# font using this format, however.
#
# FT_PIXEL_MODE_GRAY4	
# A 4-bit per pixel bitmap, representing embedded anti-aliased bitmaps in font
# files according to the OpenType specification. We haven't found a single font
# using this format, however.
#
# FT_PIXEL_MODE_LCD	
# An 8-bit bitmap, representing RGB or BGR decimated glyph images used for
# display on LCD displays; the bitmap is three times wider than the original
# glyph image. See also FT_RENDER_MODE_LCD.
#
# FT_PIXEL_MODE_LCD_V	
# An 8-bit bitmap, representing RGB or BGR decimated glyph images used for
# display on rotated LCD displays; the bitmap is three times taller than the
# original glyph image. See also FT_RENDER_MODE_LCD_V.
#
FT_PIXEL_MODES = {'FT_PIXEL_MODE_NONE' : 0,
                  'FT_PIXEL_MODE_MONO' : 1,
                  'FT_PIXEL_MODE_GRAY' : 2,
                  'FT_PIXEL_MODE_GRAY2': 3,
                  'FT_PIXEL_MODE_GRAY4': 4,
                  'FT_PIXEL_MODE_LCD'  : 5,
                  'FT_PIXEL_MODE_LCD_V': 6,
                  'FT_PIXEL_MODE_MAX'  : 7}
globals().update(FT_PIXEL_MODES)
ft_pixel_mode_none  = FT_PIXEL_MODE_NONE
ft_pixel_mode_mono  = FT_PIXEL_MODE_MONO
ft_pixel_mode_grays = FT_PIXEL_MODE_GRAY
ft_pixel_mode_pal2  = FT_PIXEL_MODE_GRAY2
ft_pixel_mode_pal4  = FT_PIXEL_MODE_GRAY4


# -----------------------------------------------------------------------------
# The mode how the values of FT_Glyph_Get_CBox are returned.
#
# FT_GLYPH_BBOX_UNSCALED	
# Return unscaled font units.
#
# FT_GLYPH_BBOX_SUBPIXELS
# Return unfitted 26.6 coordinates.
#
# FT_GLYPH_BBOX_GRIDFIT	
# Return grid-fitted 26.6 coordinates.
#
# FT_GLYPH_BBOX_TRUNCATE	
# Return coordinates in integer pixels.
#
# FT_GLYPH_BBOX_PIXELS	
# Return grid-fitted pixel coordinates.
#
FT_GLYPH_BBOX_MODES = {'FT_GLYPH_BBOX_UNSCALED'  : 0,
                       'FT_GLYPH_BBOX_SUBPIXELS' : 0,
                       'FT_GLYPH_BBOX_GRIDFIT'   : 1,
                       'FT_GLYPH_BBOX_TRUNCATE'  : 2,
                       'FT_GLYPH_BBOX_PIXELS'    : 3}
globals().update(FT_GLYPH_BBOX_MODES)



# -----------------------------------------------------------------------------
# An enumeration type used to describe the format of a given glyph image. Note
# that this version of FreeType only supports two image formats, even though
# future font drivers will be able to register their own format.
#
# FT_GLYPH_FORMAT_NONE	
# The value 0 is reserved.

# FT_GLYPH_FORMAT_COMPOSITE
# The glyph image is a composite of several other images. This format is only
# used with FT_LOAD_NO_RECURSE, and is used to report compound glyphs (like
# accented characters).
#
# FT_GLYPH_FORMAT_BITMAP	
# The glyph image is a bitmap, and can be described as an FT_Bitmap. You
# generally need to access the 'bitmap' field of the FT_GlyphSlotRec structure
# to read it.
#
# FT_GLYPH_FORMAT_OUTLINE
# The glyph image is a vectorial outline made of line segments and Bezier arcs;
# it can be described as an FT_Outline; you generally want to access the
# 'outline' field of the FT_GlyphSlotRec structure to read it.
#
# FT_GLYPH_FORMAT_PLOTTER
# The glyph image is a vectorial path with no inside and outside contours. Some
# Type 1 fonts, like those in the Hershey family, contain glyphs in this
# format. These are described as FT_Outline, but FreeType isn't currently
# capable of rendering them correctly.
#
def _FT_IMAGE_TAG(a,b,c,d):
    return ( ord(a) << 24 | ord(b) << 16 | ord(c) << 8 | ord(d) )
FT_GLYPH_FORMATS = {
    'FT_GLYPH_FORMAT_NONE'      : _FT_IMAGE_TAG( '\0','\0','\0','\0' ),
    'FT_GLYPH_FORMAT_COMPOSITE' : _FT_IMAGE_TAG( 'c','o','m','p' ),
    'FT_GLYPH_FORMAT_BITMAP'    : _FT_IMAGE_TAG( 'b','i','t','s' ),
    'FT_GLYPH_FORMAT_OUTLINE'   : _FT_IMAGE_TAG( 'o','u','t','l' ),
    'FT_GLYPH_FORMAT_PLOTTER'   : _FT_IMAGE_TAG( 'p','l','o','t' )}
globals().update(FT_GLYPH_FORMATS)
ft_glyph_format_none      = FT_GLYPH_FORMAT_NONE
ft_glyph_format_composite = FT_GLYPH_FORMAT_COMPOSITE
ft_glyph_format_bitmap    = FT_GLYPH_FORMAT_BITMAP
ft_glyph_format_outline   = FT_GLYPH_FORMAT_OUTLINE
ft_glyph_format_plotter   = FT_GLYPH_FORMAT_PLOTTER



# -----------------------------------------------------------------------------
# An enumeration used to specify character sets supported by charmaps. Used in
# the FT_Select_Charmap API function.
#
# FT_ENCODING_NONE	
# The encoding value 0 is reserved.
#
# FT_ENCODING_UNICODE	
# Corresponds to the Unicode character set. This value covers all versions of
# the Unicode repertoire, including ASCII and Latin-1. Most fonts include a
# Unicode charmap, but not all of them.
#
# For example, if you want to access Unicode value U+1F028 (and the font
# contains it), use value 0x1F028 as the input value for FT_Get_Char_Index.
#
# FT_ENCODING_MS_SYMBOL	
# Corresponds to the Microsoft Symbol encoding, used to encode mathematical
# symbols in the 32..255 character code range. For more information, see
# 'http://www.ceviz.net/symbol.htm'.
#
# FT_ENCODING_SJIS	
# Corresponds to Japanese SJIS encoding. More info at at
# 'http://langsupport.japanreference.com/encoding.shtml'. See note on
# multi-byte encodings below.
#
# FT_ENCODING_GB2312	
# Corresponds to an encoding system for Simplified Chinese as used used in
# mainland China.
#
# FT_ENCODING_BIG5	
# Corresponds to an encoding system for Traditional Chinese as used in Taiwan
# and Hong Kong.
#
# FT_ENCODING_WANSUNG	
# Corresponds to the Korean encoding system known as Wansung. For more
# information see 'http://www.microsoft.com/typography/unicode/949.txt'.
#
# FT_ENCODING_JOHAB	
# The Korean standard character set (KS C 5601-1992), which corresponds to MS
# Windows code page 1361. This character set includes all possible Hangeul
# character combinations.
#
# FT_ENCODING_ADOBE_LATIN_1
# Corresponds to a Latin-1 encoding as defined in a Type 1 PostScript font. It
# is limited to 256 character codes.
#
# FT_ENCODING_ADOBE_STANDARD
# Corresponds to the Adobe Standard encoding, as found in Type 1, CFF, and
# OpenType/CFF fonts. It is limited to 256 character codes.
#
# FT_ENCODING_ADOBE_EXPERT
# Corresponds to the Adobe Expert encoding, as found in Type 1, CFF, and
# OpenType/CFF fonts. It is limited to 256 character codes.
#
# FT_ENCODING_ADOBE_CUSTOM
# Corresponds to a custom encoding, as found in Type 1, CFF, and OpenType/CFF
# fonts. It is limited to 256 character codes.

# FT_ENCODING_APPLE_ROMAN
# Corresponds to the 8-bit Apple roman encoding. Many TrueType and OpenType
# fonts contain a charmap for this encoding, since older versions of Mac OS are
# able to use it.
#
# FT_ENCODING_OLD_LATIN_2
# This value is deprecated and was never used nor reported by FreeType. Don't
# use or test for it.
#
def _FT_ENC_TAG(a,b,c,d):
    return ( ord(a) << 24 | ord(b) << 16 | ord(c) << 8 | ord(d) )
FT_ENCODINGS = {'FT_ENCODING_NONE'           : _FT_ENC_TAG('\0','\0','\0','\0'),
                'FT_ENCODING_MS_SYMBOL'      : _FT_ENC_TAG( 's','y','m','b' ),
                'FT_ENCODING_UNICODE'        : _FT_ENC_TAG( 'u','n','i','c' ),
                'FT_ENCODING_SJIS'           : _FT_ENC_TAG( 's','j','i','s' ),
                'FT_ENCODING_GB2312'         : _FT_ENC_TAG( 'g','b',' ',' ' ),
                'FT_ENCODING_BIG5'           : _FT_ENC_TAG( 'b','i','g','5' ),
                'FT_ENCODING_WANSUNG'        : _FT_ENC_TAG( 'w','a','n','s' ),
                'FT_ENCODING_JOHAB'          : _FT_ENC_TAG( 'j','o','h','a' ),
                'FT_ENCODING_ADOBE_STANDARD' : _FT_ENC_TAG( 'A','D','O','B' ),
                'FT_ENCODING_ADOBE_EXPERT'   : _FT_ENC_TAG( 'A','D','B','E' ),
                'FT_ENCODING_ADOBE_CUSTOM'   : _FT_ENC_TAG( 'A','D','B','C' ),
                'FT_ENCODING_ADOBE_LATIN1'   : _FT_ENC_TAG( 'l','a','t','1' ),
                'FT_ENCODING_OLD_LATIN2'     : _FT_ENC_TAG( 'l','a','t','2' ),
                'FT_ENCODING_APPLE_ROMAN'    : _FT_ENC_TAG( 'a','r','m','n' ) }
globals().update(FT_ENCODINGS)



# -----------------------------------------------------------------------------
# An enumeration type that lists the render modes supported by FreeType 2. Each
# mode corresponds to a specific type of scanline conversion performed on the
# outline.
#
# For bitmap fonts and embedded bitmaps the 'bitmap->pixel_mode' field in the
# FT_GlyphSlotRec structure gives the format of the returned bitmap.
#
# All modes except FT_RENDER_MODE_MONO use 256 levels of opacity.
#
# FT_RENDER_MODE_NORMAL	
# This is the default render mode; it corresponds to 8-bit anti-aliased
# bitmaps.
#
# FT_RENDER_MODE_LIGHT	
# This is equivalent to FT_RENDER_MODE_NORMAL. It is only defined as a separate
# value because render modes are also used indirectly to define hinting
# algorithm selectors. See FT_LOAD_TARGET_XXX for details.
#
# FT_RENDER_MODE_MONO	
# This mode corresponds to 1-bit bitmaps (with 2 levels of opacity).
#
# FT_RENDER_MODE_LCD	
# This mode corresponds to horizontal RGB and BGR sub-pixel displays like LCD
# screens. It produces 8-bit bitmaps that are 3 times the width of the original
# glyph outline in pixels, and which use the FT_PIXEL_MODE_LCD mode.
#
# FT_RENDER_MODE_LCD_V	
# This mode corresponds to vertical RGB and BGR sub-pixel displays (like PDA
# screens, rotated LCD displays, etc.). It produces 8-bit bitmaps that are 3
# times the height of the original glyph outline in pixels and use the
# FT_PIXEL_MODE_LCD_V mode.
#
FT_RENDER_MODES = { 'FT_RENDER_MODE_NORMAL' : 0,
                    'FT_RENDER_MODE_LIGHT'  : 1,
                    'FT_RENDER_MODE_MONO'   : 2,
                    'FT_RENDER_MODE_LCD'    : 3,
                    'FT_RENDER_MODE_LCD_V'  : 4 }
globals().update(FT_RENDER_MODES)



# -----------------------------------------------------------------------------
# A list of values that are used to select a specific hinting algorithm to use
# by the hinter. You should OR one of these values to your 'load_flags' when
# calling FT_Load_Glyph.
#
# Note that font's native hinters may ignore the hinting algorithm you have
# specified (e.g., the TrueType bytecode interpreter). You can set
# FT_LOAD_FORCE_AUTOHINT to ensure that the auto-hinter is used.
#
# Also note that FT_LOAD_TARGET_LIGHT is an exception, in that it always
# implies FT_LOAD_FORCE_AUTOHINT.
#
# FT_LOAD_TARGET_NORMAL	
# This corresponds to the default hinting algorithm, optimized for standard
# gray-level rendering. For monochrome output, use FT_LOAD_TARGET_MONO instead.
#
# FT_LOAD_TARGET_LIGHT	
# A lighter hinting algorithm for non-monochrome modes. Many generated glyphs
# are more fuzzy but better resemble its original shape. A bit like rendering
# on Mac OS X.
#
# As a special exception, this target implies FT_LOAD_FORCE_AUTOHINT.
#
# FT_LOAD_TARGET_MONO	
# Strong hinting algorithm that should only be used for monochrome output. The
# result is probably unpleasant if the glyph is rendered in non-monochrome
# modes.
#
# FT_LOAD_TARGET_LCD	
# A variant of FT_LOAD_TARGET_NORMAL optimized for horizontally decimated LCD
# displays.
#
# FT_LOAD_TARGET_LCD_V	
# A variant of FT_LOAD_TARGET_NORMAL optimized for vertically decimated LCD
# displays.

def _FT_LOAD_TARGET_(x):
    return (x & 15) << 16
FT_LOAD_TARGETS = {
    'FT_LOAD_TARGET_NORMAL' : _FT_LOAD_TARGET_(FT_RENDER_MODE_NORMAL),
    'FT_LOAD_TARGET_LIGHT'  : _FT_LOAD_TARGET_(FT_RENDER_MODE_LIGHT),
    'FT_LOAD_TARGET_MONO'   : _FT_LOAD_TARGET_(FT_RENDER_MODE_MONO),
    'FT_LOAD_TARGET_LCD'    : _FT_LOAD_TARGET_(FT_RENDER_MODE_LCD),
    'FT_LOAD_TARGET_LCD_V'  : _FT_LOAD_TARGET_(FT_RENDER_MODE_LCD_V) }
globals().update(FT_LOAD_TARGETS)
#def FT_LOAD_TARGET_MODE(x):
#    return (x >> 16) & 15


# -----------------------------------------------------------------------------
# A list of bit-field constants used with FT_Load_Glyph to indicate what kind
# of operations to perform during glyph loading.
#
# FT_LOAD_DEFAULT	
# Corresponding to 0, this value is used as the default glyph load
# operation. In this case, the following happens:
#
# 1. FreeType looks for a bitmap for the glyph corresponding to the face's
# current size. If one is found, the function returns. The bitmap data can be
# accessed from the glyph slot (see note below).
#
# 2. If no embedded bitmap is searched or found, FreeType looks for a scalable
# outline. If one is found, it is loaded from the font file, scaled to device
# pixels, then 'hinted' to the pixel grid in order to optimize it. The outline
# data can be accessed from the glyph slot (see note below).
#
# Note that by default, the glyph loader doesn't render outlines into
# bitmaps. The following flags are used to modify this default behaviour to
# more specific and useful cases.
#
# FT_LOAD_NO_SCALE	
# Don't scale the outline glyph loaded, but keep it in font units.
#
# This flag implies FT_LOAD_NO_HINTING and FT_LOAD_NO_BITMAP, and unsets
# FT_LOAD_RENDER.
#
# FT_LOAD_NO_HINTING	
# Disable hinting. This generally generates 'blurrier' bitmap glyph when the
# glyph is rendered in any of the anti-aliased modes. See also the note below.
#
# This flag is implied by FT_LOAD_NO_SCALE.
#
# FT_LOAD_RENDER	
# Call FT_Render_Glyph after the glyph is loaded. By default, the glyph is
# rendered in FT_RENDER_MODE_NORMAL mode. This can be overridden by
# FT_LOAD_TARGET_XXX or FT_LOAD_MONOCHROME.
#
# This flag is unset by FT_LOAD_NO_SCALE.
#
# FT_LOAD_NO_BITMAP	
# Ignore bitmap strikes when loading. Bitmap-only fonts ignore this flag.
#
# FT_LOAD_NO_SCALE always sets this flag.
#
# FT_LOAD_VERTICAL_LAYOUT
# Load the glyph for vertical text layout. Don't use it as it is problematic
# currently.
#
# FT_LOAD_FORCE_AUTOHINT	
# Indicates that the auto-hinter is preferred over the font's native
# hinter. See also the note below.
#
# FT_LOAD_CROP_BITMAP	
# Indicates that the font driver should crop the loaded bitmap glyph (i.e.,
# remove all space around its black bits). Not all drivers implement this.
#
# FT_LOAD_PEDANTIC	
# Indicates that the font driver should perform pedantic verifications during
# glyph loading. This is mostly used to detect broken glyphs in fonts. By
# default, FreeType tries to handle broken fonts also.
#
# FT_LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH
# Indicates that the font driver should ignore the global advance width defined
# in the font. By default, that value is used as the advance width for all
# glyphs when the face has FT_FACE_FLAG_FIXED_WIDTH set.
#
# This flag exists for historical reasons (to support buggy CJK fonts).
#
# FT_LOAD_NO_RECURSE	
# This flag is only used internally. It merely indicates that the font driver
# should not load composite glyphs recursively. Instead, it should set the
# 'num_subglyph' and 'subglyphs' values of the glyph slot accordingly, and set
# 'glyph->format' to FT_GLYPH_FORMAT_COMPOSITE.
#
# The description of sub-glyphs is not available to client applications for now.
#
# This flag implies FT_LOAD_NO_SCALE and FT_LOAD_IGNORE_TRANSFORM.
#
# FT_LOAD_IGNORE_TRANSFORM
# Indicates that the transform matrix set by FT_Set_Transform should be ignored.
#
# FT_LOAD_MONOCHROME	
# This flag is used with FT_LOAD_RENDER to indicate that you want to render an
# outline glyph to a 1-bit monochrome bitmap glyph, with 8 pixels packed into
# each byte of the bitmap data.
#
# Note that this has no effect on the hinting algorithm used. You should rather
# use FT_LOAD_TARGET_MONO so that the monochrome-optimized hinting algorithm is
# used.
#
# FT_LOAD_LINEAR_DESIGN	
# Indicates that the 'linearHoriAdvance' and 'linearVertAdvance' fields of
# FT_GlyphSlotRec should be kept in font units. See FT_GlyphSlotRec for
# details.
#
# FT_LOAD_NO_AUTOHINT	
# Disable auto-hinter. See also the note below.
#
FT_LOAD_FLAGS = { 'FT_LOAD_DEFAULT'                      : 0x0,
                  'FT_LOAD_NO_SCALE'                     : 0x1,
                  'FT_LOAD_NO_HINTING'                   : 0x2,
                  'FT_LOAD_RENDER'                       : 0x4,
                  'FT_LOAD_NO_BITMAP'                    : 0x8,
                  'FT_LOAD_VERTICAL_LAYOUT'              : 0x10,
                  'FT_LOAD_FORCE_AUTOHINT'               : 0x20,
                  'FT_LOAD_CROP_BITMAP'                  : 0x40,
                  'FT_LOAD_PEDANTIC'                     : 0x80,
                  'FT_LOAD_IGNORE_GLOBAL_ADVANCE_WIDTH'  : 0x200,
                  'FT_LOAD_NO_RECURSE'                   : 0x400,
                  'FT_LOAD_IGNORE_TRANSFORM'             : 0x800,
                  'FT_LOAD_MONOCHROME'                   : 0x1000,
                  'FT_LOAD_LINEAR_DESIGN'                : 0x2000,
                  'FT_LOAD_NO_AUTOHINT'                  : 0x8000 }
globals().update(FT_LOAD_FLAGS)



# -----------------------------------------------------------------------------
# A list of bit-flags used to indicate the style of a given face. These are
# used in the 'style_flags' field of FT_FaceRec.
#
# FT_STYLE_FLAG_ITALIC	
# Indicates that a given face style is italic or oblique.
#
# FT_STYLE_FLAG_BOLD	
# Indicates that a given face is bold.
#
FT_STYLE_FLAGS = {'FT_STYLE_FLAG_ITALIC' : 1,
                  'FT_STYLE_FLAG_BOLD'   : 2 }
globals().update(FT_STYLE_FLAGS)



# -----------------------------------------------------------------------------
# A list of bit flags used in the 'face_flags' field of the FT_FaceRec
# structure. They inform client applications of properties of the corresponding
# face.
#
# FT_FACE_FLAG_SCALABLE	
# Indicates that the face contains outline glyphs. This doesn't prevent bitmap
# strikes, i.e., a face can have both this and and FT_FACE_FLAG_FIXED_SIZES
# set.
#
# FT_FACE_FLAG_FIXED_SIZES
# Indicates that the face contains bitmap strikes. See also the
# 'num_fixed_sizes' and 'available_sizes' fields of FT_FaceRec.
#
# FT_FACE_FLAG_FIXED_WIDTH
# Indicates that the face contains fixed-width characters (like Courier,
# Lucido, MonoType, etc.).
#
# FT_FACE_FLAG_SFNT	
# Indicates that the face uses the 'sfnt' storage scheme. For now, this means
# TrueType and OpenType.
#
# FT_FACE_FLAG_HORIZONTAL
# Indicates that the face contains horizontal glyph metrics. This should be set
# for all common formats.
#
# FT_FACE_FLAG_VERTICAL	
# Indicates that the face contains vertical glyph metrics. This is only
# available in some formats, not all of them.
#
# FT_FACE_FLAG_KERNING	
# Indicates that the face contains kerning information. If set, the kerning
# distance can be retrieved through the function FT_Get_Kerning. Otherwise the
# function always return the vector (0,0). Note that FreeType doesn't handle
# kerning data from the 'GPOS' table (as present in some OpenType fonts).
#
#
# FT_FACE_FLAG_MULTIPLE_MASTERS
# Indicates that the font contains multiple masters and is capable of
# interpolating between them. See the multiple-masters specific API for
# details.
#
# FT_FACE_FLAG_GLYPH_NAMES
# Indicates that the font contains glyph names that can be retrieved through
# FT_Get_Glyph_Name. Note that some TrueType fonts contain broken glyph name
# tables. Use the function FT_Has_PS_Glyph_Names when needed.
#
# FT_FACE_FLAG_EXTERNAL_STREAM
# Used internally by FreeType to indicate that a face's stream was provided by
# the client application and should not be destroyed when FT_Done_Face is
# called. Don't read or test this flag.
#
# FT_FACE_FLAG_HINTER	
# Set if the font driver has a hinting machine of its own. For example, with
# TrueType fonts, it makes sense to use data from the SFNT 'gasp' table only if
# the native TrueType hinting engine (with the bytecode interpreter) is
# available and active.
#
# FT_FACE_FLAG_CID_KEYED	
# Set if the font is CID-keyed. In that case, the font is not accessed by glyph
# indices but by CID values. For subsetted CID-keyed fonts this has the
# consequence that not all index values are a valid argument to
# FT_Load_Glyph. Only the CID values for which corresponding glyphs in the
# subsetted font exist make FT_Load_Glyph return successfully; in all other
# cases you get an 'FT_Err_Invalid_Argument' error.
#
# Note that CID-keyed fonts which are in an SFNT wrapper don't have this flag
# set since the glyphs are accessed in the normal way (using contiguous
# indices); the 'CID-ness' isn't visible to the application.
#
# FT_FACE_FLAG_TRICKY	
# Set if the font is 'tricky', this is, it always needs the font format's
# native hinting engine to get a reasonable result. A typical example is the
# Chinese font 'mingli.ttf' which uses TrueType bytecode instructions to move
# and scale all of its subglyphs.
#
# It is not possible to autohint such fonts using FT_LOAD_FORCE_AUTOHINT; it
# will also ignore FT_LOAD_NO_HINTING. You have to set both FT_LOAD_NO_HINTING
# and FT_LOAD_NO_AUTOHINT to really disable hinting; however, you probably
# never want this except for demonstration purposes.
#
# Currently, there are six TrueType fonts in the list of tricky fonts; they are
# hard-coded in file 'ttobjs.c'.
#
FT_FACE_FLAGS = { 'FT_FACE_FLAG_SCALABLE'          : 1 <<  0,
                  'FT_FACE_FLAG_FIXED_SIZES'       : 1 <<  1,
                  'FT_FACE_FLAG_FIXED_WIDTH'       : 1 <<  2,
                  'FT_FACE_FLAG_SFNT'              : 1 <<  3,
                  'FT_FACE_FLAG_HORIZONTAL'        : 1 <<  4,
                  'FT_FACE_FLAG_VERTICAL'          : 1 <<  5,
                  'FT_FACE_FLAG_KERNING'           : 1 <<  6,
                  'FT_FACE_FLAG_FAST_GLYPHS'       : 1 <<  7,
                  'FT_FACE_FLAG_MULTIPLE_MASTERS'  : 1 <<  8,
                  'FT_FACE_FLAG_GLYPH_NAMES'       : 1 <<  9,
                  'FT_FACE_FLAG_EXTERNAL_STREAM'   : 1 << 10,
                  'FT_FACE_FLAG_HINTER'            : 1 << 11 }
globals().update(FT_FACE_FLAGS)



# -----------------------------------------------------------------------------
# A list of bit-field constants use for the flags in an outline's 'flags'
# field.
#
# FT_OUTLINE_NONE	
# Value 0 is reserved.
#
# FT_OUTLINE_OWNER	
# If set, this flag indicates that the outline's field arrays (i.e., 'points',
# 'flags', and 'contours') are 'owned' by the outline object, and should thus
# be freed when it is destroyed.
#
# FT_OUTLINE_EVEN_ODD_FILL
# By default, outlines are filled using the non-zero winding rule. If set to 1,
# the outline will be filled using the even-odd fill rule (only works with the
# smooth rasterizer).
#
# FT_OUTLINE_REVERSE_FILL
# By default, outside contours of an outline are oriented in clock-wise
# direction, as defined in the TrueType specification. This flag is set if the
# outline uses the opposite direction (typically for Type 1 fonts). This flag
# is ignored by the scan converter.
#
# FT_OUTLINE_IGNORE_DROPOUTS
# By default, the scan converter will try to detect drop-outs in an outline and
# correct the glyph bitmap to ensure consistent shape continuity. If set, this
# flag hints the scan-line converter to ignore such cases. See below for more
# information.
#
# FT_OUTLINE_SMART_DROPOUTS
# Select smart dropout control. If unset, use simple dropout control. Ignored
# if FT_OUTLINE_IGNORE_DROPOUTS is set. See below for more information.
#
# FT_OUTLINE_INCLUDE_STUBS
# If set, turn pixels on for 'stubs', otherwise exclude them. Ignored if
# FT_OUTLINE_IGNORE_DROPOUTS is set. See below for more information.
#
# FT_OUTLINE_HIGH_PRECISION
# This flag indicates that the scan-line converter should try to convert this
# outline to bitmaps with the highest possible quality. It is typically set for
# small character sizes. Note that this is only a hint that might be completely
# ignored by a given scan-converter.
#
# FT_OUTLINE_SINGLE_PASS	
# This flag is set to force a given scan-converter to only use a single pass
# over the outline to render a bitmap glyph image. Normally, it is set for very
# large character sizes. It is only a hint that might be completely ignored by
# a given scan-converter.
#
FT_OUTLINE_FLAGS = { 'FT_OUTLINE_NONE'            : 0x0,
                     'FT_OUTLINE_OWNER'           : 0x1,
                     'FT_OUTLINE_EVEN_ODD_FILL'   : 0x2,
                     'FT_OUTLINE_REVERSE_FILL'    : 0x4,
                     'FT_OUTLINE_IGNORE_DROPOUTS' : 0x8,
                     'FT_OUTLINE_SMART_DROPOUTS'  : 0x10,
                     'FT_OUTLINE_INCLUDE_STUBS'   : 0x20,
                     'FT_OUTLINE_HIGH_PRECISION'  : 0x100,
                     'FT_OUTLINE_SINGLE_PASS'     : 0x200 }
globals().update(FT_OUTLINE_FLAGS)



# -----------------------------------------------------------------------------
# A list of bit-field constants used within the 'flags' field of the
# FT_Open_Args structure.
# 
# FT_OPEN_MEMORY	
# This is a memory-based stream.
#
# FT_OPEN_STREAM	
# Copy the stream from the 'stream' field.
#
# FT_OPEN_PATHNAME	
# Create a new input stream from a C path name.
#
# FT_OPEN_DRIVER	
# Use the 'driver' field.
#
# FT_OPEN_PARAMS	
# Use the 'num_params' and 'params' fields.
#
FT_OPEN_MODES = {'FT_OPEN_MEMORY':   0x1,
                 'FT_OPEN_STREAM':   0x2,
                 'FT_OPEN_PATHNAME': 0x4,
                 'FT_OPEN_DRIVER':   0x8,
                 'FT_OPEN_PARAMS':   0x10 }
globals().update(FT_OPEN_MODES)



# -----------------------------------------------------------------------------
# An enumeration used to specify which kerning values to return in
# FT_Get_Kerning.
#
# FT_KERNING_DEFAULT	
# Return scaled and grid-fitted kerning distances (value is 0).
#
# FT_KERNING_UNFITTED	
# Return scaled but un-grid-fitted kerning distances.
#
# FT_KERNING_UNSCALED	
# Return the kerning vector in original font units.
#
FT_KERNING_MODES = { 'FT_KERNING_DEFAULT'  : 0,
                     'FT_KERNING_UNFITTED' : 1,
                     'FT_KERNING_UNSCALED' : 2 }
globals().update(FT_KERNING_MODES)



# -----------------------------------------------------------------------------
# These values determine how two joining lines are rendered in a stroker.
#
# FT_STROKER_LINEJOIN_ROUND
# Used to render rounded line joins. Circular arcs are used to join two lines
# smoothly.
#
# FT_STROKER_LINEJOIN_BEVEL
# Used to render beveled line joins; i.e., the two joining lines are extended
# until they intersect.
#
# FT_STROKER_LINEJOIN_MITER
# Same as beveled rendering, except that an additional line break is added if
# the angle between the two joining lines is too closed (this is useful to
# avoid unpleasant spikes in beveled rendering).
#
FT_STROKER_LINEJOINS = { 'FT_STROKER_LINEJOIN_ROUND' : 0,
                         'FT_STROKER_LINEJOIN_BEVEL' : 1,
                         'FT_STROKER_LINEJOIN_MITER' : 2}
globals().update(FT_STROKER_LINEJOINS)



# -----------------------------------------------------------------------------
# These values determine how the end of opened sub-paths are rendered in a
# stroke.
#
# FT_STROKER_LINECAP_BUTT
# The end of lines is rendered as a full stop on the last point itself.
#
# FT_STROKER_LINECAP_ROUND
# The end of lines is rendered as a half-circle around the last point.
#
# FT_STROKER_LINECAP_SQUARE
# The end of lines is rendered as a square around the last point.
#
FT_STROKER_LINECAPS = { 'FT_STROKER_LINECAP_BUTT'   : 0,
                        'FT_STROKER_LINECAP_ROUND'  : 1,
                        'FT_STROKER_LINECAP_SQUARE' : 2}
globals().update(FT_STROKER_LINECAPS)



# -----------------------------------------------------------------------------
# These values are used to select a given stroke border in
# FT_Stroker_GetBorderCounts and FT_Stroker_ExportBorder.
#
# FT_STROKER_BORDER_LEFT	
# Select the left border, relative to the drawing direction.
#
# FT_STROKER_BORDER_RIGHT
# Select the right border, relative to the drawing direction.
#
# Note
# Applications are generally interested in the 'inside' and 'outside'
# borders. However, there is no direct mapping between these and the 'left' and
# 'right' ones, since this really depends on the glyph's drawing orientation,
# which varies between font formats.
#
# You can however use FT_Outline_GetInsideBorder and
# FT_Outline_GetOutsideBorder to get these.
#
FT_STROKER_BORDERS = { 'FT_STROKER_BORDER_LEFT'  : 0,
                       'FT_STROKER_BORDER_RIGHT' : 1}
globals().update(FT_STROKER_BORDERS)



# -----------------------------------------------------------------------------
# A list of values to identify various types of LCD filters.
#
# FT_LCD_FILTER_NONE	
# Do not perform filtering. When used with subpixel rendering, this results in
# sometimes severe color fringes.
#
# FT_LCD_FILTER_DEFAULT	
# The default filter reduces color fringes considerably, at the cost of a
# slight blurriness in the output.
#
# FT_LCD_FILTER_LIGHT	
# The light filter is a variant that produces less blurriness at the cost of
# slightly more color fringes than the default one. It might be better,
# depending on taste, your monitor, or your personal vision.
#
# FT_LCD_FILTER_LEGACY	
# This filter corresponds to the original libXft color filter. It provides high
# contrast output but can exhibit really bad color fringes if glyphs are not
# extremely well hinted to the pixel grid. In other words, it only works well
# if the TrueType bytecode interpreter is enabled and high-quality hinted fonts
# are used.
#
# This filter is only provided for comparison purposes, and might be disabled
# or stay unsupported in the future.

FT_LCD_FILTERS = {'FT_LCD_FILTER_NONE'    : 0,
                  'FT_LCD_FILTER_DEFAULT' : 1,
                  'FT_LCD_FILTER_LIGHT'   : 2,
                  'FT_LCD_FILTER_LEGACY'  : 16}
globals().update(FT_LCD_FILTERS)



# -----------------------------------------------------------------------------
# A list of valid values for the 'platform_id' identifier code in FT_CharMapRec
# and FT_SfntName structures.
#
# TT_PLATFORM_APPLE_UNICODE
# Used by Apple to indicate a Unicode character map and/or name entry. See
# TT_APPLE_ID_XXX for corresponding 'encoding_id' values. Note that name
# entries in this format are coded as big-endian UCS-2 character codes only.
#
# TT_PLATFORM_MACINTOSH	
# Used by Apple to indicate a MacOS-specific charmap and/or name entry. See
# TT_MAC_ID_XXX for corresponding 'encoding_id' values. Note that most TrueType
# fonts contain an Apple roman charmap to be usable on MacOS systems (even if
# they contain a Microsoft charmap as well).
#
# TT_PLATFORM_ISO	
# This value was used to specify ISO/IEC 10646 charmaps. It is however now
# deprecated. See TT_ISO_ID_XXX for a list of corresponding 'encoding_id'
# values.
#
# TT_PLATFORM_MICROSOFT	
# Used by Microsoft to indicate Windows-specific charmaps. See TT_MS_ID_XXX for
# a list of corresponding 'encoding_id' values. Note that most fonts contain a
# Unicode charmap using (TT_PLATFORM_MICROSOFT, TT_MS_ID_UNICODE_CS).
#
# TT_PLATFORM_CUSTOM	
# Used to indicate application-specific charmaps.
#
# TT_PLATFORM_ADOBE	
# This value isn't part of any font format specification, but is used by
# FreeType to report Adobe-specific charmaps in an FT_CharMapRec structure. See
# TT_ADOBE_ID_XXX.

TT_PLATFORMS = {
    'TT_PLATFORM_APPLE_UNICODE' : 0,
    'TT_PLATFORM_MACINTOSH'     : 1,
    'TT_PLATFORM_ISO'           : 2, # deprecated
    'TT_PLATFORM_MICROSOFT'     : 3,
    'TT_PLATFORM_CUSTOM'        : 4,
    'TT_PLATFORM_ADOBE'         : 7} # artificial
globals().update(TT_PLATFORMS)


# -----------------------------------------------------------------------------
# A list of valid values for the 'encoding_id' for TT_PLATFORM_APPLE_UNICODE
# charmaps and name entries.
#
# TT_APPLE_ID_DEFAULT	
# Unicode version 1.0.
#
# TT_APPLE_ID_UNICODE_1_1
# Unicode 1.1; specifies Hangul characters starting at U+34xx.
#
# TT_APPLE_ID_ISO_10646	
# Deprecated (identical to preceding).
#
# TT_APPLE_ID_UNICODE_2_0
# Unicode 2.0 and beyond (UTF-16 BMP only).
#
# TT_APPLE_ID_UNICODE_32	
# Unicode 3.1 and beyond, using UTF-32.
#
# TT_APPLE_ID_VARIANT_SELECTOR
# From Adobe, not Apple. Not a normal cmap. Specifies variations on a real
# cmap.
TT_APPLE_IDS = {
    'TT_APPLE_ID_DEFAULT'          : 0,
    'TT_APPLE_ID_UNICODE_1_1'      : 1,
    'TT_APPLE_ID_ISO_10646'        : 2,
    'TT_APPLE_ID_UNICODE_2_0'      : 3,
    'TT_APPLE_ID_UNICODE_32'       : 4,
    'TT_APPLE_ID_VARIANT_SELECTOR' : 5 }
globals().update(TT_APPLE_IDS)



# -----------------------------------------------------------------------------
# A list of valid values for the 'encoding_id' for TT_PLATFORM_MACINTOSH
# charmaps and name entries.
TT_MAC_IDS = {
    'TT_MAC_ID_ROMAN'               :  0,
    'TT_MAC_ID_JAPANESE'            :  1,
    'TT_MAC_ID_TRADITIONAL_CHINESE' :  2,
    'TT_MAC_ID_KOREAN'              :  3,
    'TT_MAC_ID_ARABIC'              :  4,
    'TT_MAC_ID_HEBREW'              :  5,
    'TT_MAC_ID_GREEK'               :  6,
    'TT_MAC_ID_RUSSIAN'             :  7,
    'TT_MAC_ID_RSYMBOL'             :  8,
    'TT_MAC_ID_DEVANAGARI'          :  9,
    'TT_MAC_ID_GURMUKHI'            : 10,
    'TT_MAC_ID_GUJARATI'            : 11,
    'TT_MAC_ID_ORIYA'               : 12,
    'TT_MAC_ID_BENGALI'             : 13,
    'TT_MAC_ID_TAMIL'               : 14,
    'TT_MAC_ID_TELUGU'              : 15,
    'TT_MAC_ID_KANNADA'             : 16,
    'TT_MAC_ID_MALAYALAM'           : 17,
    'TT_MAC_ID_SINHALESE'           : 18,
    'TT_MAC_ID_BURMESE'             : 19,
    'TT_MAC_ID_KHMER'               : 20,
    'TT_MAC_ID_THAI'                : 21,
    'TT_MAC_ID_LAOTIAN'             : 22,
    'TT_MAC_ID_GEORGIAN'            : 23,
    'TT_MAC_ID_ARMENIAN'            : 24,
    'TT_MAC_ID_MALDIVIAN'           : 25,
    'TT_MAC_ID_SIMPLIFIED_CHINESE'  : 25,
    'TT_MAC_ID_TIBETAN'             : 26,
    'TT_MAC_ID_MONGOLIAN'           : 27,
    'TT_MAC_ID_GEEZ'                : 28,
    'TT_MAC_ID_SLAVIC'              : 29,
    'TT_MAC_ID_VIETNAMESE'          : 30,
    'TT_MAC_ID_SINDHI'              : 31,
    'TT_MAC_ID_UNINTERP'            : 32}
globals().update(TT_MAC_IDS)


# -----------------------------------------------------------------------------
# A list of valid values for the 'encoding_id' for TT_PLATFORM_MICROSOFT
# charmaps and name entries.
#
# TT_MS_ID_SYMBOL_CS	
# Corresponds to Microsoft symbol encoding. See FT_ENCODING_MS_SYMBOL.
#
# TT_MS_ID_UNICODE_CS	
# Corresponds to a Microsoft WGL4 charmap, matching Unicode. See
# FT_ENCODING_UNICODE.
#
# TT_MS_ID_SJIS	
# Corresponds to SJIS Japanese encoding. See FT_ENCODING_SJIS.
#
# TT_MS_ID_GB2312	
# Corresponds to Simplified Chinese as used in Mainland China. See
# FT_ENCODING_GB2312.
#
# TT_MS_ID_BIG_5	
# Corresponds to Traditional Chinese as used in Taiwan and Hong Kong. See
# FT_ENCODING_BIG5.
#
# TT_MS_ID_WANSUNG	
# Corresponds to Korean Wansung encoding. See FT_ENCODING_WANSUNG.
#
# TT_MS_ID_JOHAB	
# Corresponds to Johab encoding. See FT_ENCODING_JOHAB.
#
# TT_MS_ID_UCS_4	
# Corresponds to UCS-4 or UTF-32 charmaps. This has been added to the OpenType
# specification version 1.4 (mid-2001.)

TT_MS_IDS = {
    'TT_MS_ID_SYMBOL_CS'  :  0,
    'TT_MS_ID_UNICODE_CS' :  1,
    'TT_MS_ID_SJIS'       :  2,
    'TT_MS_ID_GB2312'     :  3,
    'TT_MS_ID_BIG_5'      :  4,
    'TT_MS_ID_WANSUNG'    :  5,
    'TT_MS_ID_JOHAB'      :  6,
    'TT_MS_ID_UCS_4'      : 10 }
globals().update(TT_MS_IDS)


# -----------------------------------------------------------------------------
# A list of valid values for the 'encoding_id' for TT_PLATFORM_ADOBE
# charmaps. This is a FreeType-specific extension!
#
# TT_ADOBE_ID_STANDARD	
# Adobe standard encoding.
#
# TT_ADOBE_ID_EXPERT	
# Adobe expert encoding.
#
# TT_ADOBE_ID_CUSTOM	
# Adobe custom encoding.
#
# TT_ADOBE_ID_LATIN_1	
# Adobe Latin 1 encoding.

TT_ADOBE_IDS = {
    'TT_ADOBE_ID_STANDARD' : 0,
    'TT_ADOBE_ID_EXPERT'   : 1,
    'TT_ADOBE_ID_CUSTOM'   : 2,
    'TT_ADOBE_ID_LATIN_1'  : 3 }
globals().update(TT_ADOBE_IDS)


# -----------------------------------------------------------------------------
#  Possible values of the language identifier field in the name records of the
#  TTF `name' table if the `platform' identifier code is TT_PLATFORM_MACINTOSH.
TT_MAC_LANGIDS = {
    'TT_MAC_LANGID_ENGLISH'                    :   0,
    'TT_MAC_LANGID_FRENCH'                     :   1,
    'TT_MAC_LANGID_GERMAN'                     :   2,
    'TT_MAC_LANGID_ITALIAN'                    :   3,
    'TT_MAC_LANGID_DUTCH'                      :   4,
    'TT_MAC_LANGID_SWEDISH'                    :   5,
    'TT_MAC_LANGID_SPANISH'                    :   6,
    'TT_MAC_LANGID_DANISH'                     :   7,
    'TT_MAC_LANGID_PORTUGUESE'                 :   8,
    'TT_MAC_LANGID_NORWEGIAN'                  :   9,
    'TT_MAC_LANGID_HEBREW'                     :  10,
    'TT_MAC_LANGID_JAPANESE'                   :  11,
    'TT_MAC_LANGID_ARABIC'                     :  12,
    'TT_MAC_LANGID_FINNISH'                    :  13,
    'TT_MAC_LANGID_GREEK'                      :  14,
    'TT_MAC_LANGID_ICELANDIC'                  :  15,
    'TT_MAC_LANGID_MALTESE'                    :  16,
    'TT_MAC_LANGID_TURKISH'                    :  17,
    'TT_MAC_LANGID_CROATIAN'                   :  18,
    'TT_MAC_LANGID_CHINESE_TRADITIONAL'        :  19,
    'TT_MAC_LANGID_URDU'                       :  20,
    'TT_MAC_LANGID_HINDI'                      :  21,
    'TT_MAC_LANGID_THAI'                       :  22,
    'TT_MAC_LANGID_KOREAN'                     :  23,
    'TT_MAC_LANGID_LITHUANIAN'                 :  24,
    'TT_MAC_LANGID_POLISH'                     :  25,
    'TT_MAC_LANGID_HUNGARIAN'                  :  26,
    'TT_MAC_LANGID_ESTONIAN'                   :  27,
    'TT_MAC_LANGID_LETTISH'                    :  28,
    'TT_MAC_LANGID_SAAMISK'                    :  29,
    'TT_MAC_LANGID_FAEROESE'                   :  30,
    'TT_MAC_LANGID_FARSI'                      :  31,
    'TT_MAC_LANGID_RUSSIAN'                    :  32,
    'TT_MAC_LANGID_CHINESE_SIMPLIFIED'         :  33,
    'TT_MAC_LANGID_FLEMISH'                    :  34,
    'TT_MAC_LANGID_IRISH'                      :  35,
    'TT_MAC_LANGID_ALBANIAN'                   :  36,
    'TT_MAC_LANGID_ROMANIAN'                   :  37,
    'TT_MAC_LANGID_CZECH'                      :  38,
    'TT_MAC_LANGID_SLOVAK'                     :  39,
    'TT_MAC_LANGID_SLOVENIAN'                  :  40,
    'TT_MAC_LANGID_YIDDISH'                    :  41,
    'TT_MAC_LANGID_SERBIAN'                    :  42,
    'TT_MAC_LANGID_MACEDONIAN'                 :  43,
    'TT_MAC_LANGID_BULGARIAN'                  :  44,
    'TT_MAC_LANGID_UKRAINIAN'                  :  45,
    'TT_MAC_LANGID_BYELORUSSIAN'               :  46,
    'TT_MAC_LANGID_UZBEK'                      :  47,
    'TT_MAC_LANGID_KAZAKH'                     :  48,
    'TT_MAC_LANGID_AZERBAIJANI'                :  49,
    'TT_MAC_LANGID_AZERBAIJANI_CYRILLIC_SCRIPT':  49,
    'TT_MAC_LANGID_AZERBAIJANI_ARABIC_SCRIPT'  :  50,
    'TT_MAC_LANGID_ARMENIAN'                   :  51,
    'TT_MAC_LANGID_GEORGIAN'                   :  52,
    'TT_MAC_LANGID_MOLDAVIAN'                  :  53,
    'TT_MAC_LANGID_KIRGHIZ'                    :  54,
    'TT_MAC_LANGID_TAJIKI'                     :  55,
    'TT_MAC_LANGID_TURKMEN'                    :  56,
    'TT_MAC_LANGID_MONGOLIAN'                  :  57,
    'TT_MAC_LANGID_MONGOLIAN_MONGOLIAN_SCRIPT' :  57,
    'TT_MAC_LANGID_MONGOLIAN_CYRILLIC_SCRIPT'  :  58,
    'TT_MAC_LANGID_PASHTO'                     :  59,
    'TT_MAC_LANGID_KURDISH'                    :  60,
    'TT_MAC_LANGID_KASHMIRI'                   :  61,
    'TT_MAC_LANGID_SINDHI'                     :  62,
    'TT_MAC_LANGID_TIBETAN'                    :  63,
    'TT_MAC_LANGID_NEPALI'                     :  64,
    'TT_MAC_LANGID_SANSKRIT'                   :  65,
    'TT_MAC_LANGID_MARATHI'                    :  66,
    'TT_MAC_LANGID_BENGALI'                    :  67,
    'TT_MAC_LANGID_ASSAMESE'                   :  68,
    'TT_MAC_LANGID_GUJARATI'                   :  69,
    'TT_MAC_LANGID_PUNJABI'                    :  70,
    'TT_MAC_LANGID_ORIYA'                      :  71,
    'TT_MAC_LANGID_MALAYALAM'                  :  72,
    'TT_MAC_LANGID_KANNADA'                    :  73,
    'TT_MAC_LANGID_TAMIL'                      :  74,
    'TT_MAC_LANGID_TELUGU'                     :  75,
    'TT_MAC_LANGID_SINHALESE'                  :  76,
    'TT_MAC_LANGID_BURMESE'                    :  77,
    'TT_MAC_LANGID_KHMER'                      :  78,
    'TT_MAC_LANGID_LAO'                        :  79,
    'TT_MAC_LANGID_VIETNAMESE'                 :  80,
    'TT_MAC_LANGID_INDONESIAN'                 :  81,
    'TT_MAC_LANGID_TAGALOG'                    :  82,
    'TT_MAC_LANGID_MALAY_ROMAN_SCRIPT'         :  83,
    'TT_MAC_LANGID_MALAY_ARABIC_SCRIPT'        :  84,
    'TT_MAC_LANGID_AMHARIC'                    :  85,
    'TT_MAC_LANGID_TIGRINYA'                   :  86,
    'TT_MAC_LANGID_GALLA'                      :  87,
    'TT_MAC_LANGID_SOMALI'                     :  88,
    'TT_MAC_LANGID_SWAHILI'                    :  89,
    'TT_MAC_LANGID_RUANDA'                     :  90,
    'TT_MAC_LANGID_RUNDI'                      :  91,
    'TT_MAC_LANGID_CHEWA'                      :  92,
    'TT_MAC_LANGID_MALAGASY'                   :  93,
    'TT_MAC_LANGID_ESPERANTO'                  :  94,
    'TT_MAC_LANGID_WELSH'                      : 128,
    'TT_MAC_LANGID_BASQUE'                     : 129,
    'TT_MAC_LANGID_CATALAN'                    : 130,
    'TT_MAC_LANGID_LATIN'                      : 131,
    'TT_MAC_LANGID_QUECHUA'                    : 132,
    'TT_MAC_LANGID_GUARANI'                    : 133,
    'TT_MAC_LANGID_AYMARA'                     : 134,
    'TT_MAC_LANGID_TATAR'                      : 135,
    'TT_MAC_LANGID_UIGHUR'                     : 136,
    'TT_MAC_LANGID_DZONGKHA'                   : 137,
    'TT_MAC_LANGID_JAVANESE'                   : 138,
    'TT_MAC_LANGID_SUNDANESE'                  : 139,
    'TT_MAC_LANGID_GALICIAN'                   : 140,
    'TT_MAC_LANGID_AFRIKAANS'                  : 141,
    'TT_MAC_LANGID_BRETON'                     : 142,
    'TT_MAC_LANGID_INUKTITUT'                  : 143,
    'TT_MAC_LANGID_SCOTTISH_GAELIC'            : 144,
    'TT_MAC_LANGID_MANX_GAELIC'                : 145,
    'TT_MAC_LANGID_IRISH_GAELIC'               : 146,
    'TT_MAC_LANGID_TONGAN'                     : 147,
    'TT_MAC_LANGID_GREEK_POLYTONIC'            : 148,
    'TT_MAC_LANGID_GREELANDIC'                 : 149,
    'TT_MAC_LANGID_AZERBAIJANI_ROMAN_SCRIPT'   : 150 }
globals().update(TT_MAC_LANGIDS)



# -----------------------------------------------------------------------------
# Possible values of the language identifier field in the name records of the
# TTF `name' table if the `platform' identifier code is TT_PLATFORM_MICROSOFT.

TT_MS_LANGIDS = {
    'TT_MS_LANGID_ARABIC_GENERAL'                    : 0x0001,
    'TT_MS_LANGID_ARABIC_SAUDI_ARABIA'               : 0x0401,
    'TT_MS_LANGID_ARABIC_IRAQ'                       : 0x0801,
    'TT_MS_LANGID_ARABIC_EGYPT'                      : 0x0c01,
    'TT_MS_LANGID_ARABIC_LIBYA'                      : 0x1001,
    'TT_MS_LANGID_ARABIC_ALGERIA'                    : 0x1401,
    'TT_MS_LANGID_ARABIC_MOROCCO'                    : 0x1801,
    'TT_MS_LANGID_ARABIC_TUNISIA'                    : 0x1c01,
    'TT_MS_LANGID_ARABIC_OMAN'                       : 0x2001,
    'TT_MS_LANGID_ARABIC_YEMEN'                      : 0x2401,
    'TT_MS_LANGID_ARABIC_SYRIA'                      : 0x2801,
    'TT_MS_LANGID_ARABIC_JORDAN'                     : 0x2c01,
    'TT_MS_LANGID_ARABIC_LEBANON'                    : 0x3001,
    'TT_MS_LANGID_ARABIC_KUWAIT'                     : 0x3401,
    'TT_MS_LANGID_ARABIC_UAE'                        : 0x3801,
    'TT_MS_LANGID_ARABIC_BAHRAIN'                    : 0x3c01,
    'TT_MS_LANGID_ARABIC_QATAR'                      : 0x4001,
    'TT_MS_LANGID_BULGARIAN_BULGARIA'                : 0x0402,
    'TT_MS_LANGID_CATALAN_SPAIN'                     : 0x0403,
    'TT_MS_LANGID_CHINESE_GENERAL'                   : 0x0004,
    'TT_MS_LANGID_CHINESE_TAIWAN'                    : 0x0404,
    'TT_MS_LANGID_CHINESE_PRC'                       : 0x0804,
    'TT_MS_LANGID_CHINESE_HONG_KONG'                 : 0x0c04,
    'TT_MS_LANGID_CHINESE_SINGAPORE'                 : 0x1004,
    'TT_MS_LANGID_CHINESE_MACAU'                     : 0x1404,
    'TT_MS_LANGID_CZECH_CZECH_REPUBLIC'              : 0x0405,
    'TT_MS_LANGID_DANISH_DENMARK'                    : 0x0406,
    'TT_MS_LANGID_GERMAN_GERMANY'                    : 0x0407,
    'TT_MS_LANGID_GERMAN_SWITZERLAND'                : 0x0807,
    'TT_MS_LANGID_GERMAN_AUSTRIA'                    : 0x0c07,
    'TT_MS_LANGID_GERMAN_LUXEMBOURG'                 : 0x1007,
    'TT_MS_LANGID_GERMAN_LIECHTENSTEI'               : 0x1407,
    'TT_MS_LANGID_GREEK_GREECE'                      : 0x0408,
    'TT_MS_LANGID_ENGLISH_GENERAL'                   : 0x0009,
    'TT_MS_LANGID_ENGLISH_UNITED_STATES'             : 0x0409,
    'TT_MS_LANGID_ENGLISH_UNITED_KINGDOM'            : 0x0809,
    'TT_MS_LANGID_ENGLISH_AUSTRALIA'                 : 0x0c09,
    'TT_MS_LANGID_ENGLISH_CANADA'                    : 0x1009,
    'TT_MS_LANGID_ENGLISH_NEW_ZEALAND'               : 0x1409,
    'TT_MS_LANGID_ENGLISH_IRELAND'                   : 0x1809,
    'TT_MS_LANGID_ENGLISH_SOUTH_AFRICA'              : 0x1c09,
    'TT_MS_LANGID_ENGLISH_JAMAICA'                   : 0x2009,
    'TT_MS_LANGID_ENGLISH_CARIBBEAN'                 : 0x2409,
    'TT_MS_LANGID_ENGLISH_BELIZE'                    : 0x2809,
    'TT_MS_LANGID_ENGLISH_TRINIDAD'                  : 0x2c09,
    'TT_MS_LANGID_ENGLISH_ZIMBABWE'                  : 0x3009,
    'TT_MS_LANGID_ENGLISH_PHILIPPINES'               : 0x3409,
    'TT_MS_LANGID_ENGLISH_INDONESIA'                 : 0x3809,
    'TT_MS_LANGID_ENGLISH_HONG_KONG'                 : 0x3c09,
    'TT_MS_LANGID_ENGLISH_INDIA'                     : 0x4009,
    'TT_MS_LANGID_ENGLISH_MALAYSIA'                  : 0x4409,
    'TT_MS_LANGID_ENGLISH_SINGAPORE'                 : 0x4809,
    'TT_MS_LANGID_SPANISH_SPAIN_TRADITIONAL_SORT'    : 0x040a,
    'TT_MS_LANGID_SPANISH_MEXICO'                    : 0x080a,
    'TT_MS_LANGID_SPANISH_SPAIN_INTERNATIONAL_SORT'  : 0x0c0a,
    'TT_MS_LANGID_SPANISH_GUATEMALA'                 : 0x100a,
    'TT_MS_LANGID_SPANISH_COSTA_RICA'                : 0x140a,
    'TT_MS_LANGID_SPANISH_PANAMA'                    : 0x180a,
    'TT_MS_LANGID_SPANISH_DOMINICAN_REPUBLIC'        : 0x1c0a,
    'TT_MS_LANGID_SPANISH_VENEZUELA'                 : 0x200a,
    'TT_MS_LANGID_SPANISH_COLOMBIA'                  : 0x240a,
    'TT_MS_LANGID_SPANISH_PERU'                      : 0x280a,
    'TT_MS_LANGID_SPANISH_ARGENTINA'                 : 0x2c0a,
    'TT_MS_LANGID_SPANISH_ECUADOR'                   : 0x300a,
    'TT_MS_LANGID_SPANISH_CHILE'                     : 0x340a,
    'TT_MS_LANGID_SPANISH_URUGUAY'                   : 0x380a,
    'TT_MS_LANGID_SPANISH_PARAGUAY'                  : 0x3c0a,
    'TT_MS_LANGID_SPANISH_BOLIVIA'                   : 0x400a,
    'TT_MS_LANGID_SPANISH_EL_SALVADOR'               : 0x440a,
    'TT_MS_LANGID_SPANISH_HONDURAS'                  : 0x480a,
    'TT_MS_LANGID_SPANISH_NICARAGUA'                 : 0x4c0a,
    'TT_MS_LANGID_SPANISH_PUERTO_RICO'               : 0x500a,
    'TT_MS_LANGID_SPANISH_UNITED_STATES'             : 0x540a,
    'TT_MS_LANGID_SPANISH_LATIN_AMERICA'             : 0xE40a,
    'TT_MS_LANGID_FINNISH_FINLAND'                   : 0x040b,
    'TT_MS_LANGID_FRENCH_FRANCE'                     : 0x040c,
    'TT_MS_LANGID_FRENCH_BELGIUM'                    : 0x080c,
    'TT_MS_LANGID_FRENCH_CANADA'                     : 0x0c0c,
    'TT_MS_LANGID_FRENCH_SWITZERLAND'                : 0x100c,
    'TT_MS_LANGID_FRENCH_LUXEMBOURG'                 : 0x140c,
    'TT_MS_LANGID_FRENCH_MONACO'                     : 0x180c,
    'TT_MS_LANGID_FRENCH_WEST_INDIES'                : 0x1c0c,
    'TT_MS_LANGID_FRENCH_REUNION'                    : 0x200c,
    'TT_MS_LANGID_FRENCH_CONGO'                      : 0x240c,
    'TT_MS_LANGID_FRENCH_SENEGAL'                    : 0x280c,
    'TT_MS_LANGID_FRENCH_CAMEROON'                   : 0x2c0c,
    'TT_MS_LANGID_FRENCH_COTE_D_IVOIRE'              : 0x300c,
    'TT_MS_LANGID_FRENCH_MALI'                       : 0x340c,
    'TT_MS_LANGID_FRENCH_MOROCCO'                    : 0x380c,
    'TT_MS_LANGID_FRENCH_HAITI'                      : 0x3c0c,
    'TT_MS_LANGID_FRENCH_NORTH_AFRICA'               : 0xE40c,
    'TT_MS_LANGID_HEBREW_ISRAEL'                     : 0x040d,
    'TT_MS_LANGID_HUNGARIAN_HUNGARY'                 : 0x040e,
    'TT_MS_LANGID_ICELANDIC_ICELAND'                 : 0x040f,
    'TT_MS_LANGID_ITALIAN_ITALY'                     : 0x0410,
    'TT_MS_LANGID_ITALIAN_SWITZERLAND'               : 0x0810,
    'TT_MS_LANGID_JAPANESE_JAPAN'                    : 0x0411,
    'TT_MS_LANGID_KOREAN_EXTENDED_WANSUNG_KOREA'     : 0x0412,
    'TT_MS_LANGID_KOREAN_JOHAB_KOREA'                : 0x0812,
    'TT_MS_LANGID_DUTCH_NETHERLANDS'                 : 0x0413,
    'TT_MS_LANGID_DUTCH_BELGIUM'                     : 0x0813,
    'TT_MS_LANGID_NORWEGIAN_NORWAY_BOKMAL'           : 0x0414,
    'TT_MS_LANGID_NORWEGIAN_NORWAY_NYNORSK'          : 0x0814,
    'TT_MS_LANGID_POLISH_POLAND'                     : 0x0415,
    'TT_MS_LANGID_PORTUGUESE_BRAZIL'                 : 0x0416,
    'TT_MS_LANGID_PORTUGUESE_PORTUGAL'               : 0x0816,
    'TT_MS_LANGID_RHAETO_ROMANIC_SWITZERLAND'        : 0x0417,
    'TT_MS_LANGID_ROMANIAN_ROMANIA'                  : 0x0418,
    'TT_MS_LANGID_MOLDAVIAN_MOLDAVIA'                : 0x0818,
    'TT_MS_LANGID_RUSSIAN_RUSSIA'                    : 0x0419,
    'TT_MS_LANGID_RUSSIAN_MOLDAVIA'                  : 0x0819,
    'TT_MS_LANGID_CROATIAN_CROATIA'                  : 0x041a,
    'TT_MS_LANGID_SERBIAN_SERBIA_LATIN'              : 0x081a,
    'TT_MS_LANGID_SERBIAN_SERBIA_CYRILLIC'           : 0x0c1a,
    'TT_MS_LANGID_CROATIAN_BOSNIA_HERZEGOVINA'       : 0x101a,
    'TT_MS_LANGID_BOSNIAN_BOSNIA_HERZEGOVINA'        : 0x141a,
    'TT_MS_LANGID_SERBIAN_BOSNIA_HERZ_LATIN'         : 0x181a,
    'TT_MS_LANGID_SERBIAN_BOSNIA_HERZ_CYRILLIC'      : 0x181a,
    'TT_MS_LANGID_SLOVAK_SLOVAKIA'                   : 0x041b,
    'TT_MS_LANGID_ALBANIAN_ALBANIA'                  : 0x041c,
    'TT_MS_LANGID_SWEDISH_SWEDEN'                    : 0x041d,
    'TT_MS_LANGID_SWEDISH_FINLAND'                   : 0x081d,
    'TT_MS_LANGID_THAI_THAILAND'                     : 0x041e,
    'TT_MS_LANGID_TURKISH_TURKEY'                    : 0x041f,
    'TT_MS_LANGID_URDU_PAKISTAN'                     : 0x0420,
    'TT_MS_LANGID_URDU_INDIA'                        : 0x0820,
    'TT_MS_LANGID_INDONESIAN_INDONESIA'              : 0x0421,
    'TT_MS_LANGID_UKRAINIAN_UKRAINE'                 : 0x0422,
    'TT_MS_LANGID_BELARUSIAN_BELARUS'                : 0x0423,
    'TT_MS_LANGID_SLOVENE_SLOVENIA'                  : 0x0424,
    'TT_MS_LANGID_ESTONIAN_ESTONIA'                  : 0x0425,
    'TT_MS_LANGID_LATVIAN_LATVIA'                    : 0x0426,
    'TT_MS_LANGID_LITHUANIAN_LITHUANIA'              : 0x0427,
    'TT_MS_LANGID_CLASSIC_LITHUANIAN_LITHUANIA'      : 0x0827,
    'TT_MS_LANGID_TAJIK_TAJIKISTAN'                  : 0x0428,
    'TT_MS_LANGID_FARSI_IRAN'                        : 0x0429,
    'TT_MS_LANGID_VIETNAMESE_VIET_NAM'               : 0x042a,
    'TT_MS_LANGID_ARMENIAN_ARMENIA'                  : 0x042b,
    'TT_MS_LANGID_AZERI_AZERBAIJAN_LATIN'            : 0x042c,
    'TT_MS_LANGID_AZERI_AZERBAIJAN_CYRILLIC'         : 0x082c,
    'TT_MS_LANGID_BASQUE_SPAIN'                      : 0x042d,
    'TT_MS_LANGID_SORBIAN_GERMANY'                   : 0x042e,
    'TT_MS_LANGID_MACEDONIAN_MACEDONIA'              : 0x042f,
    'TT_MS_LANGID_SUTU_SOUTH_AFRICA'                 : 0x0430,
    'TT_MS_LANGID_TSONGA_SOUTH_AFRICA'               : 0x0431,
    'TT_MS_LANGID_TSWANA_SOUTH_AFRICA'               : 0x0432,
    'TT_MS_LANGID_VENDA_SOUTH_AFRICA'                : 0x0433,
    'TT_MS_LANGID_XHOSA_SOUTH_AFRICA'                : 0x0434,
    'TT_MS_LANGID_ZULU_SOUTH_AFRICA'                 : 0x0435,
    'TT_MS_LANGID_AFRIKAANS_SOUTH_AFRICA'            : 0x0436,
    'TT_MS_LANGID_GEORGIAN_GEORGIA'                  : 0x0437,
    'TT_MS_LANGID_FAEROESE_FAEROE_ISLANDS'           : 0x0438,
    'TT_MS_LANGID_HINDI_INDIA'                       : 0x0439,
    'TT_MS_LANGID_MALTESE_MALTA'                     : 0x043a,
    'TT_MS_LANGID_SAMI_NORTHERN_NORWAY'              : 0x043b,
    'TT_MS_LANGID_SAMI_NORTHERN_SWEDEN'              : 0x083b,
    'TT_MS_LANGID_SAMI_NORTHERN_FINLAND'             : 0x0C3b,
    'TT_MS_LANGID_SAMI_LULE_NORWAY'                  : 0x103b,
    'TT_MS_LANGID_SAMI_LULE_SWEDEN'                  : 0x143b,
    'TT_MS_LANGID_SAMI_SOUTHERN_NORWAY'              : 0x183b,
    'TT_MS_LANGID_SAMI_SOUTHERN_SWEDEN'              : 0x1C3b,
    'TT_MS_LANGID_SAMI_SKOLT_FINLAND'                : 0x203b,
    'TT_MS_LANGID_SAMI_INARI_FINLAND'                : 0x243b,
    'TT_MS_LANGID_SAAMI_LAPONIA'                     : 0x043b,
    'TT_MS_LANGID_SCOTTISH_GAELIC_UNITED_KINGDOM'    : 0x083c,
    'TT_MS_LANGID_IRISH_GAELIC_IRELAND'              : 0x043c,
    'TT_MS_LANGID_YIDDISH_GERMANY'                   : 0x043d,
    'TT_MS_LANGID_MALAY_MALAYSIA'                    : 0x043e,
    'TT_MS_LANGID_MALAY_BRUNEI_DARUSSALAM'           : 0x083e,
    'TT_MS_LANGID_KAZAK_KAZAKSTAN'                   : 0x043f,
    'TT_MS_LANGID_KIRGHIZ_KIRGHIZSTAN'               : 0x0440,
    'TT_MS_LANGID_KIRGHIZ_KIRGHIZ_REPUBLIC'          : 0x0440,
    'TT_MS_LANGID_SWAHILI_KENYA'                     : 0x0441,
    'TT_MS_LANGID_TURKMEN_TURKMENISTAN'              : 0x0442,
    'TT_MS_LANGID_UZBEK_UZBEKISTAN_LATIN'            : 0x0443,
    'TT_MS_LANGID_UZBEK_UZBEKISTAN_CYRILLIC'         : 0x0843,
    'TT_MS_LANGID_TATAR_TATARSTAN'                   : 0x0444,
    'TT_MS_LANGID_BENGALI_INDIA'                     : 0x0445,
    'TT_MS_LANGID_BENGALI_BANGLADESH'                : 0x0845,
    'TT_MS_LANGID_PUNJABI_INDIA'                     : 0x0446,
    'TT_MS_LANGID_PUNJABI_ARABIC_PAKISTAN'           : 0x0846,
    'TT_MS_LANGID_GUJARATI_INDIA'                    : 0x0447,
    'TT_MS_LANGID_ORIYA_INDIA'                       : 0x0448,
    'TT_MS_LANGID_TAMIL_INDIA'                       : 0x0449,
    'TT_MS_LANGID_TELUGU_INDIA'                      : 0x044a,
    'TT_MS_LANGID_KANNADA_INDIA'                     : 0x044b,
    'TT_MS_LANGID_MALAYALAM_INDIA'                   : 0x044c,
    'TT_MS_LANGID_ASSAMESE_INDIA'                    : 0x044d,
    'TT_MS_LANGID_MARATHI_INDIA'                     : 0x044e,
    'TT_MS_LANGID_SANSKRIT_INDIA'                    : 0x044f,
    'TT_MS_LANGID_MONGOLIAN_MONGOLIA'                : 0x0450,
    'TT_MS_LANGID_MONGOLIAN_MONGOLIA_MONGOLIAN'      : 0x0850,
    'TT_MS_LANGID_TIBETAN_CHINA'                     : 0x0451,
    'TT_MS_LANGID_DZONGHKA_BHUTAN'                   : 0x0851,
    'TT_MS_LANGID_TIBETAN_BHUTAN'                    : 0x0851,
    'TT_MS_LANGID_WELSH_WALES'                       : 0x0452,
    'TT_MS_LANGID_KHMER_CAMBODIA'                    : 0x0453,
    'TT_MS_LANGID_LAO_LAOS'                          : 0x0454,
    'TT_MS_LANGID_BURMESE_MYANMAR'                   : 0x0455,
    'TT_MS_LANGID_GALICIAN_SPAIN'                    : 0x0456,
    'TT_MS_LANGID_KONKANI_INDIA'                     : 0x0457,
    'TT_MS_LANGID_MANIPURI_INDIA'                    : 0x0458,
    'TT_MS_LANGID_SINDHI_INDIA'                      : 0x0459,
    'TT_MS_LANGID_SINDHI_PAKISTAN'                   : 0x0859,
    'TT_MS_LANGID_SYRIAC_SYRIA'                      : 0x045a,
    'TT_MS_LANGID_SINHALESE_SRI_LANKA'               : 0x045b,
    'TT_MS_LANGID_CHEROKEE_UNITED_STATES'            : 0x045c,
    'TT_MS_LANGID_INUKTITUT_CANADA'                  : 0x045d,
    'TT_MS_LANGID_AMHARIC_ETHIOPIA'                  : 0x045e,
    'TT_MS_LANGID_TAMAZIGHT_MOROCCO'                 : 0x045f,
    'TT_MS_LANGID_TAMAZIGHT_MOROCCO_LATIN'           : 0x085f,
    'TT_MS_LANGID_KASHMIRI_PAKISTAN'                 : 0x0460,
    'TT_MS_LANGID_KASHMIRI_SASIA'                    : 0x0860,
    'TT_MS_LANGID_KASHMIRI_INDIA'                    : 0x0860,
    'TT_MS_LANGID_NEPALI_NEPAL'                      : 0x0461,
    'TT_MS_LANGID_NEPALI_INDIA'                      : 0x0861,
    'TT_MS_LANGID_FRISIAN_NETHERLANDS'               : 0x0462,
    'TT_MS_LANGID_PASHTO_AFGHANISTAN'                : 0x0463,
    'TT_MS_LANGID_FILIPINO_PHILIPPINES'              : 0x0464,
    'TT_MS_LANGID_DHIVEHI_MALDIVES'                  : 0x0465,
    'TT_MS_LANGID_DIVEHI_MALDIVES'                   : 0x0465,
    'TT_MS_LANGID_EDO_NIGERIA'                       : 0x0466,
    'TT_MS_LANGID_FULFULDE_NIGERIA'                  : 0x0467,
    'TT_MS_LANGID_HAUSA_NIGERIA'                     : 0x0468,
    'TT_MS_LANGID_IBIBIO_NIGERIA'                    : 0x0469,
    'TT_MS_LANGID_YORUBA_NIGERIA'                    : 0x046a,
    'TT_MS_LANGID_QUECHUA_BOLIVIA'                   : 0x046b,
    'TT_MS_LANGID_QUECHUA_ECUADOR'                   : 0x086b,
    'TT_MS_LANGID_QUECHUA_PERU'                      : 0x0c6b,
    'TT_MS_LANGID_SEPEDI_SOUTH_AFRICA'               : 0x046c,
    'TT_MS_LANGID_SOTHO_SOUTHERN_SOUTH_AFRICA'       : 0x046c,
    'TT_MS_LANGID_IGBO_NIGERIA'                      : 0x0470,
    'TT_MS_LANGID_KANURI_NIGERIA'                    : 0x0471,
    'TT_MS_LANGID_OROMO_ETHIOPIA'                    : 0x0472,
    'TT_MS_LANGID_TIGRIGNA_ETHIOPIA'                 : 0x0473,
    'TT_MS_LANGID_TIGRIGNA_ERYTHREA'                 : 0x0873,
    'TT_MS_LANGID_TIGRIGNA_ERYTREA'                  : 0x0873,
    'TT_MS_LANGID_GUARANI_PARAGUAY'                  : 0x0474,
    'TT_MS_LANGID_HAWAIIAN_UNITED_STATES'            : 0x0475,
    'TT_MS_LANGID_LATIN'                             : 0x0476,
    'TT_MS_LANGID_SOMALI_SOMALIA'                    : 0x0477,
    'TT_MS_LANGID_YI_CHINA'                          : 0x0478,
    'TT_MS_LANGID_PAPIAMENTU_NETHERLANDS_ANTILLES'   : 0x0479,
    'TT_MS_LANGID_UIGHUR_CHINA'                      : 0x0480,
    'TT_MS_LANGID_MAORI_NEW_ZEALAND'                 : 0x0481 }
globals().update(TT_MS_LANGIDS)


# -----------------------------------------------------------------------------
# Possible values of the 'name' identifier field in the name records of the TTF
# 'name' table.  These values are platform independent.
TT_NAME_IDS = {                                                                       
    'TT_NAME_ID_COPYRIGHT'            :  0,
    'TT_NAME_ID_FONT_FAMILY'          :  1,
    'TT_NAME_ID_FONT_SUBFAMILY'       :  2,
    'TT_NAME_ID_UNIQUE_ID'            :  3,
    'TT_NAME_ID_FULL_NAME'            :  4,
    'TT_NAME_ID_VERSION_STRING'       :  5,
    'TT_NAME_ID_PS_NAME'              :  6,
    'TT_NAME_ID_TRADEMARK'            :  7,

    # the following values are from the OpenType spec 
    'TT_NAME_ID_MANUFACTURER'         :  8,
    'TT_NAME_ID_DESIGNER'             :  9,
    'TT_NAME_ID_DESCRIPTION'          : 10,
    'TT_NAME_ID_VENDOR_URL'           : 11,
    'TT_NAME_ID_DESIGNER_URL'         : 12,
    'TT_NAME_ID_LICENSE'              : 13,
    'TT_NAME_ID_LICENSE_URL'          : 14,
    # number 15 is reserved 
    'TT_NAME_ID_PREFERRED_FAMILY'     : 16,
    'TT_NAME_ID_PREFERRED_SUBFAMILY'  : 17,
    'TT_NAME_ID_MAC_FULL_NAME'        : 18,

    # The following code is new as of 2000-01-21
    'TT_NAME_ID_SAMPLE_TEXT'          : 19,

    # This is new in OpenType 1.3 
    'TT_NAME_ID_CID_FINDFONT_NAME'    : 20,

    # This is new in OpenType 1.5 
    'TT_NAME_ID_WWS_FAMILY'           : 21,
    'TT_NAME_ID_WWS_SUBFAMILY'        : 22 }
globals().update(TT_NAME_IDS)
