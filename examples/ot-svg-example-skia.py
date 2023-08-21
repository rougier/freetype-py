#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  OT-SVG example, alternative version based on Skia
#
#  Copyright 2023 Hin-Tak Leung
#  Distributed under the terms of the new BSD license.

#  See also the other one, the rsvg-based OT-SVG example.

from freetype import *

import skia
from skia import Size, ImageInfo, ColorType, AlphaType, Canvas, PictureRecorder, Rect, ScalarNegativeInfinity, ScalarInfinity, RTreeFactory

from packaging import version
assert(version.parse(skia.__version__) > version.parse("116.0b2")), "Needs Skia-Python 116.0b2+"

pythonapi.PyMemoryView_FromMemory.restype = py_object

# include/private/base/SkFixed.h
def SkFixedToFloat(x):
    return ((x) * 1.52587890625e-5)

from math import ceil, floor

_state = None

def svg_init(ctx):
    global _state
    _state = {}
    ctx.contents.value = _state
    return FT_Err_Ok

def svg_free(ctx):
    global _state
    _state = None
    # "None" is strictly speaking a special pyobject,
    # this line does not do what it should, i.e. setting the
    # pointer to NULL.
    ctx.contents = None
    return # void

def svg_render(slot, ctx):
    state = ctx.contents.value
    dstBitmap = skia.Bitmap()
    dstBitmap.setInfo(ImageInfo.Make(slot.contents.bitmap.width, slot.contents.bitmap.rows,
                                     ColorType.kBGRA_8888_ColorType,
                                     AlphaType.kPremul_AlphaType),
                      slot.contents.bitmap.pitch)
    dstBitmap.setPixels(pythonapi.PyMemoryView_FromMemory(cast(slot.contents.bitmap.buffer, c_char_p),
                                                          slot.contents.bitmap.rows * slot.contents.bitmap.pitch,
                                                          0x200), # Read-Write
                        )
    canvas = Canvas(dstBitmap)

    canvas.clear(skia.ColorTRANSPARENT)

    canvas.translate( -state['x'], -state['y'] )
    canvas.drawPicture( state['picture'] )

    slot.contents.bitmap.pixel_mode = FT_PIXEL_MODE_BGRA
    slot.contents.bitmap.num_grays  = 256
    slot.contents.format            = FT_GLYPH_FORMAT_BITMAP

    state['picture'] = None

    return FT_Err_Ok

def svg_preset_slot(slot, cached, ctx):
    state = ctx.contents.value

    document = ctypes.cast(slot.contents.other, FT_SVG_Document)

    metrics        = SizeMetrics(document.contents.metrics)

    units_per_EM   = FT_UShort(document.contents.units_per_EM)
    end_glyph_id   = FT_UShort(document.contents.end_glyph_id)
    start_glyph_id = FT_UShort(document.contents.start_glyph_id)

    doc = ctypes.string_at(document.contents.svg_document, # not terminated
                           size=document.contents.svg_document_length)
    data = skia.Data(doc)
    svgmem = skia.MemoryStream(data)
    svg = skia.SVGDOM.MakeFromStream(svgmem)

    if (svg.containerSize().isEmpty()):
        size = Size.Make(units_per_EM.value, units_per_EM.value)
        svg.setContainerSize(size)

    recorder = PictureRecorder()

    infiniteRect = Rect.MakeLTRB(ScalarNegativeInfinity, ScalarNegativeInfinity,
                                 ScalarInfinity, ScalarInfinity)
    bboxh = RTreeFactory()()

    recordingCanvas = recorder.beginRecording(infiniteRect, bboxh)

    ftMatrix = document.contents.transform
    ftOffset = document.contents.delta

    m = skia.Matrix()
    m.setAll(
        SkFixedToFloat(ftMatrix.xx), -SkFixedToFloat(ftMatrix.xy),  SkFixedToFloat(ftOffset.x),
       -SkFixedToFloat(ftMatrix.yx),  SkFixedToFloat(ftMatrix.yy), -SkFixedToFloat(ftOffset.y),
        0                          ,  0                          ,  1                        )

    m.postScale(SkFixedToFloat(document.contents.metrics.x_scale) / 64.0,
                SkFixedToFloat(document.contents.metrics.y_scale) / 64.0)

    recordingCanvas.concat(m)

    if ( start_glyph_id.value < end_glyph_id.value ):
        id = "glyph%u" % ( slot.contents.glyph_index )
        svg.renderNode(recordingCanvas, id)
    else:
        svg.render(recordingCanvas)

    state['picture'] = recorder.finishRecordingAsPicture()
    bounds = state['picture'].cullRect()

    width  = ceil(bounds.right()) - floor(bounds.left())
    height = ceil(bounds.bottom()) - floor(bounds.top())
    x = floor(bounds.left())
    y = floor(bounds.top())

    state['x'] = x
    state['y'] = y

    slot.contents.bitmap_left = int(state['x']) # float to int conversion
    slot.contents.bitmap_top  = int(-state['y'])

    slot.contents.bitmap.rows  = ceil( height ) # float to int
    slot.contents.bitmap.width = ceil( width )

    slot.contents.bitmap.pitch = slot.contents.bitmap.width * 4

    slot.contents.bitmap.pixel_mode = FT_PIXEL_MODE_BGRA

    metrics_width  = width
    metrics_height = height

    horiBearingX =  state['x']
    horiBearingY = -state['y']

    vertBearingX = slot.contents.metrics.horiBearingX / 64.0 - slot.contents.metrics.horiAdvance / 64.0 / 2
    vertBearingY = ( slot.contents.metrics.vertAdvance / 64.0 - slot.contents.metrics.height / 64.0 ) / 2

    slot.contents.metrics.width  = int(round( width * 64 ))
    slot.contents.metrics.height = int(round( height * 64 ))

    slot.contents.metrics.horiBearingX = int( horiBearingX * 64 )
    slot.contents.metrics.horiBearingY = int( horiBearingY * 64 )
    slot.contents.metrics.vertBearingX = int( vertBearingX * 64 )
    slot.contents.metrics.vertBearingY = int( vertBearingY * 64 )

    if ( slot.contents.metrics.vertAdvance == 0 ):
        slot.contents.metrics.vertAdvance = int( height * 1.2 * 64 )

    if ( cached == False ):
        state['picture'] = None
        state['x'] = 0
        state['y'] = 0

    return FT_Err_Ok

hooks = SVG_RendererHooks(svg_init=SVG_Lib_Init_Func(svg_init),
                          svg_free=SVG_Lib_Free_Func(svg_free),
                          svg_render=SVG_Lib_Render_Func(svg_render),
                          svg_preset_slot=SVG_Lib_Preset_Slot_Func(svg_preset_slot))

########## GL drawing code from skia-python example ##########
########## - remove in windows-less usage.          ##########
import contextlib, glfw

@contextlib.contextmanager
def glfw_window():
    if not glfw.init():
        raise RuntimeError('glfw.init() failed')
    glfw.window_hint(glfw.STENCIL_BITS, 8)
    window = glfw.create_window(WIDTH, HEIGHT, '', None, None)
    glfw.make_context_current(window)
    yield window
    glfw.terminate()

@contextlib.contextmanager
def skia_surface(window):
    context = skia.GrDirectContext.MakeGL()
    (fb_width, fb_height) = glfw.get_framebuffer_size(window)
    backend_render_target = skia.GrBackendRenderTarget(
        fb_width,
        fb_height,
        0,  # sampleCnt
        0,  # stencilBits
        skia.GrGLFramebufferInfo(0, GL.GL_RGBA8))
    surface = skia.Surface.MakeFromBackendRenderTarget(
        context, backend_render_target, skia.kBottomLeft_GrSurfaceOrigin,
        skia.kRGBA_8888_ColorType, skia.ColorSpace.MakeSRGB())
    assert surface is not None
    yield surface
    context.abandonContext()
########## GL drawing code from skia-python example ##########

if __name__ == '__main__':
    import sys
    execname = sys.argv[0]

    if len(sys.argv) < 2:
        print("Example usage: %s TrajanColor-Concept.otf" % execname)
        exit(1)

    face = Face(sys.argv[1])

    face.set_char_size( 160*64 )
    library = get_handle()
    FT_Property_Set( library, b"ot-svg", b"svg-hooks", byref(hooks) ) # python 3 only syntax
    face.load_char('A', FT_LOAD_COLOR | FT_LOAD_RENDER )

    bitmap = face.glyph.bitmap
    width = face.glyph.bitmap.width
    rows = face.glyph.bitmap.rows

    if ( face.glyph.bitmap.pitch != width * 4 ):
        raise RuntimeError('pitch != width * 4 for color bitmap: Please report this.')

    from OpenGL import GL
    WIDTH, HEIGHT = 2*width, rows

    glyphBitmap = skia.Bitmap()
    glyphBitmap.setInfo(ImageInfo.Make(bitmap.width, bitmap.rows,
                                       ColorType.kBGRA_8888_ColorType,
                                       AlphaType.kPremul_AlphaType),
                        bitmap.pitch)
    glyphBitmap.setPixels(pythonapi.PyMemoryView_FromMemory(cast(bitmap._FT_Bitmap.buffer, c_char_p),
                                                            bitmap.rows * bitmap.pitch,
                                                            0x200), # Read-Write
                          )
    with glfw_window() as window:
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        with skia_surface(window) as surface:
            with surface as canvas:
                canvas.drawBitmap(glyphBitmap, 0, 0)
                canvas.drawBitmap(glyphBitmap, width/2, 0)
                canvas.drawBitmap(glyphBitmap, width, 0)
                surface.flushAndSubmit()
                glfw.swap_buffers(window)

            while (glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS
                   and not glfw.window_should_close(window)):
                glfw.wait_events()
