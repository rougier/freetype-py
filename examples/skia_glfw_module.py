# skia_glfw_module
# This file created by 2023 Hin-Tak Leung; but Copyright skia-python project:

# Adapted from https://kyamagu.github.io/skia-python/tutorial/canvas.html#opengl-window

# Typical usage:
#
#     from skia_glfw_module import glfw_window, skia_surface
#     ....
#     with glfw_window(WIDTH, HEIGHT) as window:
#     ...
#          with skia_surface(window) as surface:
#              with surface as canvas:
#                  canvas.drawStuff()
#
#              surface.flushAndSubmit()
#              glfw.swap_buffers(window)
#

import contextlib, glfw
import skia
from OpenGL import GL

@contextlib.contextmanager
def glfw_window(WIDTH, HEIGHT):
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
