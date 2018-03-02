FreeType (high-level Python API)
================================

Freetype Python provides bindings for the FreeType library. Only the high-level API is bound.

Documentation available at: http://freetype-py.readthedocs.org/en/latest/

Installation
============

There are three ways to go about this.

1. Recommended: `pip install freetype-py`. This will install the library with a bundled FreeType binary, so you're ready to go on Windows, macOS and Linux (all with 32 and 64 bit support).
2. If you don't want to or can't use the pre-built binaries, build FreeType yourself: `export FREETYPEPY_BUNDLE_FT=yesplease && python setup.py install`. This will download and compile FreeType with Harfbuzz support as specified in `setup-build-freetype.py`. Set the environment variable `PYTHON_ARCH` to 32 or 64 to explicitly set an architecture, default is whatever your host machine uses. On macOS, we will always build a 96 bit binary.
    a. Windows: You need CMake and a C and C++ compiler, e.g. the Visual Code Community 2017 distribution with the desktop C++ workload.
    b. macOS: You need CMake and the XCode tools (full IDE not necessary)
    c. Linux: You need CMake, gcc and g++. For building a 32 bit library on a 64 bit machine, you need gcc-multilib and g++-multilib (Debian) or glibc-devel.i686 and libstdc++-devel.i686 (Fedora).
3. Install just the pure Python library and let it find a system-wide installed FreeType at runtime. This is the default.

Mac users (third way)
---------------------

Freetype should be already installed on your system. If not, either install it
using `homebrew <http://brew.sh>`_ or compile it and place the library binary
file in '/usr/local/lib'.

Linux users (third way)
-----------------------

Freetype should be already installed on your system. If not, either install
relevant package from your package manager or compile from sources and place
the library binary file in '/usr/local/lib'.

Window users (third way)
------------------------

There are no official Freetype binary releases available, but they offer some
links to precompiled Windows DLLs. Please see the `FreeType Downloads
<https://www.freetype.org/download.html>`_ page for links.
You can also compile the FreeType library from source.

32-Bit vs 64-Bit on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using freetype-py on Windows with a 32-Bit version of Python, you
need the 32-Bit version of the Freetype binary. The same applies for a 64-Bit
version of Python.

Installation on Windows
~~~~~~~~~~~~~~~~~~~~~~~

Because of the way Windows searches for dll files, make sure the resulting
file is named 'freetype.dll' (and not something like Freetype245.dll).
Windows expects the library in one of the directories listed in the $PATH
environment variable. As it is not recommended to place the dll in a Windows
system folder, you can choose one of the following ways to solve this:

* Place library in a folder of your choice and edit the $PATH user
  environment variable
* Place library in a folder of your choice and edit the $PATH system
  environment variable
* For development purpose, place the library in the working directory of
  the application
* Place the library in one of the existing directories listed in $PATH

To get a complete list of all the directories in the $PATH
environment variable (user and system), open a command promt and type

.. code::

   echo %PATH%

Usage example
=============

.. code:: python

   import freetype
   face = freetype.Face("Vera.ttf")
   face.set_char_size( 48*64 )
   face.load_char('S')
   bitmap = face.glyph.bitmap
   print bitmap.buffer

Screenshots
===========

Screenshot below comes from the wordle.py example. No clever tricks here, just
brute force.

.. image:: https://raw.githubusercontent.com/rougier/freetype-py/master/doc/_static/wordle.png

Screenshots below comes from the glyph-vector.py and glyph-vectopr-2.py
examples showing how to access a glyph outline information and use it to draw
the glyph. Rendering (with Bézier curves) is done using matplotlib.

.. image:: https://raw.githubusercontent.com/rougier/freetype-py/master/doc/_static/S.png
.. image:: https://raw.githubusercontent.com/rougier/freetype-py/master/doc/_static/G.png


Screenshot below comes from the glyph-color.py showing how to draw and combine
a glyph outline with the regular glyph.

.. image:: https://raw.githubusercontent.com/rougier/freetype-py/master/doc/_static/outline.png

The screenshot below comes from the hello-world.py example showing how to draw
text in a bitmap (that has been zoomed in to show antialiasing).

.. image:: https://raw.githubusercontent.com/rougier/freetype-py/master/doc/_static/hello-world.png


The screenshot below comes from the agg-trick.py example showing an
implementation of ideas from the `Texts Rasterization Exposures
<http://agg.sourceforge.net/antigrain.com/research/font_rasterization/>`_ by
Maxim Shemarev.

.. image:: https://raw.githubusercontent.com/rougier/freetype-py/master/doc/_static/agg-trick.png


Contributors
============

* Titusz Pan (bug report)
* Ekkehard.Blanz (bug report)
* Jānis Lībeks (bug report)
* Frantisek Malina (typo)
* Tillmann Karras (bug report & fix)
* Matthew Sitton (bug report & fix)
* Tao Gong (bug report)
* Matthew Sitton (Remove raw interfaces from the __init__.py file)
* Daniel McCloy (Adde glyph_name function)
* Nikolaus Waxweiler (Setup of CI services and bundling of FreeType)
