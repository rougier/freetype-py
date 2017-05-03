# FT_Bitmap to CAIRO_SURFACE_TYPE_IMAGE module
# ============================================
#
# Copyright 2017 Hin-Tak Leung
#
# FreeType is under FTL (BSD license with an advertising clause) or GPLv2+.
# Cairo is under LGPLv2 or MPLv1.1.
#
# This is a heavily modified copy of a few routines from Lawrence D'Oliveiro[1],
# adjusted for freetype-py, and bugfix/workaround for mono-rendering [2].
#
# The bugfix/workaround requires libtiff on small-endian platforms.
#
# TODO: Look into using FreeType's FT_Bitmap_Convert() instead. However, libtiff
#      is common enough, and probably not important.
#
#[1] https://github.com/ldo/python_freetype
#    https://github.com/ldo/python_freetype_examples
#
#[2] https://github.com/ldo/python_freetype/issues/1
#    https://github.com/ldo/python_freetype_examples/issues/1
#
'''
FT_Bitmap to CAIRO_SURFACE_TYPE_IMAGE module
============================================

Converting from Freetype's FT_Bitmap to Cairo's CAIRO_SURFACE_TYPE_IMAGE

Usage:
     from bitmap_to_surface import make_image_surface

Works with cairocffi too. (Replace "from cairo ..." with "from cairocffi ...")

Limitation: Surface.create_for_data is not in the "python 3, pycairo < 1.11" combo.
'''
from freetype import FT_PIXEL_MODE_MONO, FT_PIXEL_MODE_GRAY, FT_Pointer, FT_Bitmap

from cairo import ImageSurface, FORMAT_A1, FORMAT_A8
#from cairocffi import ImageSurface, FORMAT_A1, FORMAT_A8

from array import array
from ctypes import cast, memmove, CDLL, c_void_p, c_int
from sys import byteorder

def make_image_surface(bitmap, copy = True) :
    if ( type(bitmap) == FT_Bitmap ):
        # bare FT_Bitmap
        content = bitmap
    else:
        # wrapped Bitmap instance
        content = bitmap._FT_Bitmap
    "creates a Cairo ImageSurface containing (a copy of) the Bitmap pixels."
    if content.pixel_mode == FT_PIXEL_MODE_MONO :
        cairo_format = FORMAT_A1
    elif content.pixel_mode == FT_PIXEL_MODE_GRAY :
        cairo_format = FORMAT_A8
    else :
        raise NotImplementedError("unsupported bitmap format %d" % content.pixel_mode)
    src_pitch = content.pitch
    dst_pitch = ImageSurface.format_stride_for_width(cairo_format, content.width)
    if not copy and dst_pitch == src_pitch and content.buffer != None :
        pixels = content.buffer
    else :
        pixels = to_array(content, content.pixel_mode, dst_pitch)
    result =  ImageSurface.create_for_data(
        pixels, cairo_format,
        content.width, content.rows,
        dst_pitch)
    return result

def to_array(content, pixel_mode, dst_pitch = None) :
    "returns a Python array object containing a copy of the Bitmap pixels."
    if dst_pitch == None :
        dst_pitch = content.pitch
    buffer_size = content.rows * dst_pitch
    buffer = array("B", b"0" * buffer_size)
    dstaddr = buffer.buffer_info()[0]
    srcaddr = cast(content.buffer, FT_Pointer).value
    src_pitch = content.pitch
    if dst_pitch == src_pitch :
        memmove(dstaddr, srcaddr, buffer_size)
    else :
        # have to copy a row at a time
        if src_pitch < 0 or dst_pitch < 0 :
            raise NotImplementedError("can't cope with negative bitmap pitch")
        assert dst_pitch > src_pitch
        for i in range(content.rows) :
            memmove(dstaddr, srcaddr, src_pitch)
            dstaddr += dst_pitch
            srcaddr += src_pitch
    # pillow/PIL itself requires libtiff so it is assumed to be around.
    # swap the bit-order from freetype's (MSB) to cairo's (host order) if needed
    if ( ( byteorder == 'little' ) and (pixel_mode == FT_PIXEL_MODE_MONO ) ):
        libtiff = CDLL("libtiff.so.5")
        libtiff.TIFFReverseBits.restype = None
        libtiff.TIFFReverseBits.argtypes = (c_void_p, c_int)
        libtiff.TIFFReverseBits(buffer.buffer_info()[0], buffer_size)
    return buffer
