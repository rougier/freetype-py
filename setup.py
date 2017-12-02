#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  FreeType high-level python API - copyright 2011 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
# -----------------------------------------------------------------------------
from os import path
from codecs import open
from setuptools import setup, Extension

description = """
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

You can try to install a window binaries available from the Freetype site or
you can compile it from sources. In such a case, make sure the resulting
library binaries is named 'Freetype.dll' (and not something like
Freetype245.dll) and make sure to place a copy in Windows/System32 directory.

Usage example
=============

.. code:: python

   import freetype
   face = freetype.Face("Vera.ttf")
   face.set_char_size( 48*64 )
   face.load_char('S')
   bitmap = face.glyph.bitmap
   print bitmap.buffer

Contributors
============

* Hin-Tak Leung (many fixes, cairo examples)
* Titusz Pan (bug report)
* Ekkehard.Blanz (bug report)
* Jānis Lībeks (bug report)
* Frantisek Malina (typo)
* Tillmann Karras (bug report & fix)
* Matthew Sitton (bug report & fix)
* Tao Gong (bug report)
* Matthew Sitton (Remove raw interfaces from the __init__.py file)
"""

setup( name        = 'freetype-py',
       version     = '1.1',
       description = 'Freetype python bindings',
       long_description = description,
       author      = 'Nicolas P. Rougier',
       author_email= 'Nicolas.Rougier@inria.fr',
       url         = 'https://github.com/rougier/freetype-py',
       packages    = ['freetype', 'freetype.ft_enums'],
       classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Environment :: X11 Applications',
          'Environment :: MacOS X',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Multimedia :: Graphics',
          ],
     )
