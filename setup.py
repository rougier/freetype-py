#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  FreeType high-level python API - copyright 2011 Nicolas P. Rougier
#  Distributed under the terms of the new BSD license.
# -----------------------------------------------------------------------------
from __future__ import absolute_import, print_function

import distutils
import distutils.dir_util
import distutils.file_util
import os
import subprocess
import sys
from io import open
from os import path

from setuptools import setup

if os.environ.get("FREETYPEPY_BUNDLE_FT"):
    print("# Will build and bundle FreeType.")

    from setuptools import Extension
    from setuptools.command.build_ext import build_ext
    from wheel.bdist_wheel import bdist_wheel

    class UniversalBdistWheel(bdist_wheel):
        def get_tag(self):
            return (
                'py2.py3',
                'none',
            ) + bdist_wheel.get_tag(self)[2:]

    class SharedLibrary(Extension):
        """Object that describes the library (filename) and how to make it."""
        if sys.platform == "darwin":
            suffix = ".dylib"
        elif sys.platform == "win32":
            suffix = ".dll"
        else:
            suffix = ".so"

        def __init__(self, name, cmd, cwd=".", output_dir=".", env=None):
            Extension.__init__(self, name, sources=[])
            self.cmd = cmd
            self.cwd = path.normpath(cwd)
            self.output_dir = path.normpath(output_dir)
            self.env = env or dict(os.environ)

    class SharedLibBuildExt(build_ext):
        """Object representing command to produce and install a shared
        library."""

        # Needed to make setuptools and wheel believe they're looking at an
        # extension instead of a shared library.
        def get_ext_filename(self, ext_name):
            for ext in self.extensions:
                if isinstance(ext, SharedLibrary):
                    return os.path.join(*ext_name.split('.')) + ext.suffix
            return build_ext.get_ext_filename(self, ext_name)

        def build_extension(self, ext):
            if not isinstance(ext, SharedLibrary):
                build_ext.build_extension(self, ext)
                return

            distutils.log.info("running '{}'".format(ext.cmd))
            if not self.dry_run:
                rv = subprocess.Popen(
                    ext.cmd, cwd=ext.cwd, env=ext.env, shell=True).wait()
                if rv != 0:
                    sys.exit(rv)

            lib_name = ext.name.split(".")[-1] + ext.suffix
            lib_fullpath = path.join(ext.output_dir, lib_name)
            dest_path = self.get_ext_fullpath(ext.name)

            distutils.dir_util.mkpath(
                path.dirname(dest_path),
                verbose=self.verbose,
                dry_run=self.dry_run)

            distutils.file_util.copy_file(
                lib_fullpath,
                dest_path,
                verbose=self.verbose,
                dry_run=self.dry_run)

    ext_modules = [
        SharedLibrary(
            "freetype.libfreetype",  # package.shared_lib_name
            cmd='"{}" ./setup-build-freetype.py'.format(sys.executable),
            output_dir="build/local/lib")
    ]
    cmdclass = {
        'bdist_wheel': UniversalBdistWheel,
        'build_ext': SharedLibBuildExt
    }

else:
    print("# Will use the system-provided FreeType.")
    ext_modules = []
    cmdclass = {}

description = open(
    path.join(path.abspath(path.dirname(__file__)), 'README.rst'),
    encoding='utf-8').read()

setup(
    name='freetype-py',
    use_scm_version=True,
    description='Freetype python bindings',
    long_description=description,
    author='Nicolas P. Rougier',
    author_email='Nicolas.Rougier@inria.fr',
    url='https://github.com/rougier/freetype-py',
    packages=['freetype', 'freetype.ft_enums'],
    ext_modules=ext_modules,
    zip_safe=False if ext_modules else True,
    cmdclass=cmdclass,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics',
    ],
    keywords=['freetype', 'font'],
    setup_requires=['setuptools_scm'],
)
