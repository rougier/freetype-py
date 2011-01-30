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
for _item in FT_PIXEL_MODES.items():
    _name, _mode = _item
    globals()[_name] = _mode
ft_pixel_mode_none  = FT_PIXEL_MODE_NONE
ft_pixel_mode_mono  = FT_PIXEL_MODE_MONO
ft_pixel_mode_grays = FT_PIXEL_MODE_GRAY
ft_pixel_mode_pal2  = FT_PIXEL_MODE_GRAY2
ft_pixel_mode_pal4  = FT_PIXEL_MODE_GRAY4



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
