FreeType high-level python API
==============================

Freetype python provides bindings for the FreeType library. Only the high-level API is bound.

Documentation available at: http://freetype-py.readthedocs.org/en/latest/

Installation
============

To be able to use freetype python, you need the freetype library version 2
installed on your system.

Mac users
---------

Freetype should be already installed on your system. If not, either install it
using `homebrew <http://brew.sh>`_ or compile it and place the library binary
file in '/usr/local/lib'.

Linux users
-----------

Freetype should be already installed on your system. If not, either install
relevant package from your package manager or compile from sources and place
the library binary file in '/usr/local/lib'.

Window users
------------

There are no official Freetype binary releases available, but they offer some
links to precompiled Windows DLLs. Please see the `FreeType Downloads
<https://www.freetype.org/download.html>`_ page for links.
You can also compile the FreeType library from source.

32-Bit vs 64-Bit on Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you are using freetype-py on Windows with a 32-Bit version of python, you
need the 32-Bit version of the Freetype binary. The same applies for a 64-Bit
version of python.

Installation on Windows
~~~~~~~~~~~~~~~~~~~~~~~

Because of the way Windows searches for dll files, make sure the resulting
file is named 'freetype.dll' (and not something like Freetype245.dll).
Windows expects the library in one of the directories listed in the $PATH
environment variable. As it is not recommended to place the dll in a Windows
system folder, you can choose one of the following ways to solve this:

* Place library in a folder of choice and edit the $PATH user environment variable
* Place library in a folder of choice and edit the $PATH system environment variable
* For development purpose, place the library in the working directory of application
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

.. image:: doc/_static/wordle.png

Screenshots below comes from the glyph-vector.py and glyph-vectopr-2.py
examples showing how to access a glyph outline information and use it to draw
the glyph. Rendering (with Bézier curves) is done using matplotlib.

.. image:: doc/_static/S.png
.. image:: doc/_static/G.png


Screenshot below comes from the glyph-color.py showing how to draw and combine
a glyph outline with the regular glyph.

.. image:: doc/_static/outline.png

The screenshot below comes from the hello-world.py example showing how to draw
text in a bitmap (that has been zoomed in to show antialiasing).

.. image:: doc/_static/hello-world.png


The screenshot below comes from the agg-trick.py example showing an
implementation of ideas from the `Texts Rasterization Exposures
<http://agg.sourceforge.net/antigrain.com/research/font_rasterization/>`_ by
Maxim Shemarev.

.. image:: doc/_static/agg-trick.png


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
