#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This will build a FreeType binary for bundling with freetype-py on Windows,
# Linux and macOS. The environment determines if it's a 32 or 64 bit build (on
# Windows, set $env:PYTHON_ARCH="64" for a x64 build; on Linux, set it to "32"
# to explicitly make a 32 bit build).

# It can be used stand-alone, in conjunction with setup.py and on CI services
# like Travis and Appveyor. You need CMake and some C/C++ compiler suite (e.g.
# GCC, Visual Studio Community 2017, ...)

import distutils.dir_util
import distutils.spawn
import glob
import os
import subprocess
import sys
from os import path

FREETYPE_HOST = "https://download.savannah.gnu.org/releases/freetype/"
FREETYPE_TARBALL = "freetype-2.9.tar.bz2"
FREETYPE_URL = FREETYPE_HOST + FREETYPE_TARBALL
FREETYPE_SHA256 = (
    "e6ffba3c8cef93f557d1f767d7bc3dee860ac7a3aaff588a521e081bc36f4c8a")
HARFBUZZ_HOST = "https://www.freedesktop.org/software/harfbuzz/release/"
HARFBUZZ_TARBALL = "harfbuzz-1.7.6.tar.bz2"
HARFBUZZ_URL = HARFBUZZ_HOST + HARFBUZZ_TARBALL
HARFBUZZ_SHA256 = (
    "da7bed39134826cd51e57c29f1dfbe342ccedb4f4773b1c951ff05ff383e2e9b")

root_dir = "."
build_dir = path.join(root_dir, "build")
# CMake requires an absolute path to a prefix.
prefix_dir = path.abspath(path.join(build_dir, "local"))
build_dir_ft = path.join(build_dir, FREETYPE_TARBALL.split(".tar")[0], "build")
build_dir_hb = path.join(build_dir, HARFBUZZ_TARBALL.split(".tar")[0], "build")

CMAKE_GLOBAL_SWITCHES = ('-DCMAKE_COLOR_MAKEFILE:BOOL=false '
                         '-DCMAKE_PREFIX_PATH:PATH="{}" '
                         '-DCMAKE_INSTALL_PREFIX:PATH="{}" ').format(
                             prefix_dir, prefix_dir)

# Try to use Ninja to build things if it's available. Much faster.
# On Windows, I first need to figure out how to make it aware of VC, bitness,
# etc.
if sys.platform != "win32" and distutils.spawn.find_executable("ninja"):
    CMAKE_GLOBAL_SWITCHES += "-G Ninja "

bitness = None

if sys.platform == "win32":
    if os.environ.get("PYTHON_ARCH", "") == "64":
        print("# Making a 64 bit build.")
        bitness = 64
        CMAKE_GLOBAL_SWITCHES += ('-DCMAKE_GENERATOR_PLATFORM=x64 '
                                  '-DCMAKE_GENERATOR_TOOLSET="host=x64" ')
    else:
        print("# Making a 32 bit build.")
        bitness = 32

if sys.platform == "darwin":
    print("# Making a 96 bit build.")
    CMAKE_GLOBAL_SWITCHES += ('-DCMAKE_OSX_ARCHITECTURES="x86_64;i386" '
                              '-DCMAKE_OSX_DEPLOYMENT_TARGET="10.6" '
                              '-DCMAKE_C_FLAGS="-O2" '
                              '-DCMAKE_CXX_FLAGS="-O2" ')
    bitness = 96

if "linux" in sys.platform:
    if os.environ.get("PYTHON_ARCH", "") == "32":
        print("# Making a 32 bit build.")
        # On a 64 bit Debian/Ubuntu, this needs gcc-multilib and g++-multilib.
        # On a 64 bit Fedora, install glibc-devel and libstdc++-devel.
        CMAKE_GLOBAL_SWITCHES += ('-DCMAKE_C_FLAGS="-m32 -O2" '
                                  '-DCMAKE_CXX_FLAGS="-m32 -O2" '
                                  '-DCMAKE_LD_FLAGS="-m32" ')
        bitness = 32
    else:
        print("# Making a 64 bit build.")
        CMAKE_GLOBAL_SWITCHES += ('-DCMAKE_C_FLAGS="-m64 -O2" '
                                  '-DCMAKE_CXX_FLAGS="-m64 -O2" '
                                  '-DCMAKE_LD_FLAGS="-m64" ')
        bitness = 64


def shell(cmd, cwd=None):
    """Run a shell command specified by cmd string."""
    try:  # Python2 compatibility wrapper.
        subprocess.run(cmd, shell=True, check=True, cwd=cwd)
    except AttributeError:
        rv = subprocess.Popen(cmd, cwd=cwd, shell=True).wait()
        if rv != 0:
            sys.exit(rv)


def download(url, target_path):
    """Download url to target_path."""
    try:  # Python2 compatibility wrapper.
        from urllib.request import urlretrieve
    except ImportError:
        from urllib import urlretrieve

    print("Downloading {}...".format(url))
    urlretrieve(url, target_path)


def ensure_downloaded(url, sha256_sum):
    """Download .tar.bz2 tarball at url unless already present, extract."""
    filename = path.basename(url)
    tarball = path.join(build_dir, filename)
    tarball_dir = filename.split(".tar")[0]

    if not path.exists(tarball):
        download(url, tarball)

    if not path.exists(path.join(build_dir, tarball_dir, "CMakeLists.txt")):
        import hashlib
        hasher = hashlib.sha256()
        with open(tarball, 'rb') as tb:
            hasher.update(tb.read())
        assert hasher.hexdigest() == sha256_sum

        import tarfile
        with tarfile.open(tarball, 'r:bz2') as tb:
            tb.extractall(build_dir)


distutils.dir_util.mkpath(build_dir)
distutils.dir_util.mkpath(prefix_dir)
distutils.dir_util.mkpath(build_dir_ft)
distutils.dir_util.mkpath(build_dir_hb)

ensure_downloaded(FREETYPE_URL, FREETYPE_SHA256)
ensure_downloaded(HARFBUZZ_URL, HARFBUZZ_SHA256)

print("# First, build FreeType without Harfbuzz support")
shell(
    "cmake -DBUILD_SHARED_LIBS:BOOL=false "
    "-DWITH_HarfBuzz=OFF -DWITH_PNG=OFF -DWITH_BZip2=OFF -DWITH_ZLIB=OFF "
    "{} ..".format(CMAKE_GLOBAL_SWITCHES),
    cwd=build_dir_ft)
shell("cmake --build . --config Release --target install", cwd=build_dir_ft)

print("\n# Next, build Harfbuzz and point it to the FreeType we just build.")
shell(
    "cmake -DBUILD_SHARED_LIBS:BOOL=false " +
    # https://stackoverflow.com/questions/3961446
    ("-DCMAKE_POSITION_INDEPENDENT_CODE=ON " if bitness > 32 else "") +
    "-DHB_HAVE_FREETYPE=ON -DHB_HAVE_GLIB=OFF -DHB_HAVE_CORETEXT=OFF "
    "{} ..".format(CMAKE_GLOBAL_SWITCHES),
    cwd=build_dir_hb)
shell("cmake --build . --config Release --target install", cwd=build_dir_hb)

print("\n# Lastly, rebuild FreeType, this time with Harfbuzz support.")
harfbuzz_includes = path.join(prefix_dir, "include", "harfbuzz")
shell(
    "cmake -DBUILD_SHARED_LIBS:BOOL=true -DMINGW=ON "
    "-DWITH_HarfBuzz=ON -DWITH_PNG=OFF -DWITH_BZip2=OFF -DWITH_ZLIB=OFF "
    "-DPKG_CONFIG_EXECUTABLE=\"\" "  # Prevent finding system libraries
    "-DHARFBUZZ_INCLUDE_DIRS=\"{}\" "
    "{} ..".format(harfbuzz_includes, CMAKE_GLOBAL_SWITCHES),
    cwd=build_dir_ft)
shell("cmake --build . --config Release --target install", cwd=build_dir_ft)

# Move libraries from PREFIX/bin to PREFIX/lib if need be. This keeps setup.py
# simple.
bin_so = glob.glob(path.join(prefix_dir, "bin", "*freetype*"))
for so in bin_so:
    so_target_name = path.basename(so)
    if not so_target_name.startswith("lib"):
        so_target_name = "lib" + so_target_name
    lib_path = path.join(prefix_dir, "lib", so_target_name)
    print("# Moving '{}' to '{}'".format(so, lib_path))
    os.rename(so, lib_path)
