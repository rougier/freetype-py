# This will build a FreeType binary for bundling with freetype-py on Windows,
# Linux and macOS. The environment determines if it's a 32 or 64 bit build (on
# Windows, set $env:PYTHON_ARCH="64" for a x64 build; on Linux, set it to "32"
# to explicitly make a 32 bit build).

# It can be used stand-alone, in conjunction with setup.py and on CI services
# like Travis and Appveyor. You need CMake and some C/C++ compiler suite (e.g.
# GCC, Visual Studio Community 2017, ...)

import distutils.dir_util
import distutils.file_util
import distutils.spawn
import glob
import hashlib
import os
import shutil
import ssl
import subprocess
import sys
import tarfile
import urllib
from os import path
from urllib.request import urlopen
import platform

# Needed for the GitHub Actions macOS CI runner, which appears to come without CAs.
import certifi

FREETYPE_HOST = "https://download.savannah.gnu.org/releases/freetype/"
FREETYPE_TARBALL = "freetype-2.12.0.tar.xz"
FREETYPE_URL = FREETYPE_HOST + FREETYPE_TARBALL
FREETYPE_SHA256 = "ef5c336aacc1a079ff9262d6308d6c2a066dd4d2a905301c4adda9b354399033"
HARFBUZZ_HOST = "https://github.com/harfbuzz/harfbuzz/releases/download/4.2.0/"
HARFBUZZ_TARBALL = "harfbuzz-4.2.0.tar.xz"
HARFBUZZ_URL = HARFBUZZ_HOST + HARFBUZZ_TARBALL
HARFBUZZ_SHA256 = "f2200f177768bdc21445aa09703326f3bbe8114ac083d081fe1a79d305c7ae73"

root_dir = "."
build_dir = path.join(root_dir, "build")
# CMake requires an absolute path to a prefix.
prefix_dir = path.abspath(path.join(build_dir, "local"))
lib_dir = path.join(prefix_dir, "lib")
build_dir_ft = path.join(build_dir, FREETYPE_TARBALL.split(".tar")[0], "build")
build_dir_hb = path.join(build_dir, HARFBUZZ_TARBALL.split(".tar")[0], "build")

CMAKE_GLOBAL_SWITCHES = (
    "-DCMAKE_COLOR_MAKEFILE=false "
    '-DCMAKE_PREFIX_PATH="{}" '
    '-DCMAKE_INSTALL_PREFIX="{}" '
).format(prefix_dir, prefix_dir)

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
        CMAKE_GLOBAL_SWITCHES += (
            "-DCMAKE_GENERATOR_PLATFORM=x64 " '-DCMAKE_GENERATOR_TOOLSET="host=x64" '
        )
    else:
        print("# Making a 32 bit build.")
        bitness = 32

if sys.platform == "darwin":
    print("# Making a 64 bit build.")
    CMAKE_GLOBAL_SWITCHES += (
        '-DCMAKE_OSX_ARCHITECTURES="x86_64" '
        '-DCMAKE_OSX_DEPLOYMENT_TARGET="10.9" '
        '-DCMAKE_C_FLAGS="-O2" '
        '-DCMAKE_CXX_FLAGS="-O2" '
    )
    bitness = 64

if "linux" in sys.platform:
    c_flags = cxx_flags = "-O2"
    ld_flags = ""
    if platform.machine() == "x86_64":
        if (
            os.environ.get("PYTHON_ARCH", "") == "32"
            or platform.architecture() == "32bit"
        ):
            print("# Making a 32 bit build.")
            # On a 64 bit Debian/Ubuntu, this needs gcc-multilib and g++-multilib.
            # On a 64 bit Fedora, install glibc-devel and libstdc++-devel.
            c_flags = "-m32 {}".format(c_flags)
            cxx_flags = "-m32 {}".format(cxx_flags)
            ld_flags = "-m32"
            bitness = 32
        else:
            print("# Making a 64 bit build.")
            c_flags = "-m64 {}".format(c_flags)
            cxx_flags = "-m64 {}".format(cxx_flags)
            ld_flags = "-m64"
            bitness = 64
    else:
        print("# Making a '{}' build.".format(platform.machine()))
        if platform.architecture() == "32bit":
            bitness = 32
        else:
            bitness = 64
    CMAKE_GLOBAL_SWITCHES += (
        '-DCMAKE_C_FLAGS="{}" '.format(c_flags) +
        '-DCMAKE_CXX_FLAGS="{}" '.format(cxx_flags) +
        '-DCMAKE_LD_FLAGS="{}" '.format(ld_flags)
    )


def shell(cmd, cwd=None):
    """Run a shell command specified by cmd string."""
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)


def download(url, target_path):
    """Download url to target_path."""
    print("Downloading {}...".format(url))
    # Create a custom context and fill in certifi CAs because GitHub Action's macOS CI
    # runners don't seem to have certificates installed, leading to a download
    # failure...
    context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH, cafile=certifi.where()
    )
    with urllib.request.urlopen(url, context=context) as response, open(
        target_path, "wb"
    ) as f:
        shutil.copyfileobj(response, f)


def ensure_downloaded(url, sha256_sum):
    """Download .tar.bz2 tarball at url unless already present, extract."""
    filename = path.basename(url)
    tarball = path.join(build_dir, filename)
    tarball_dir = filename.split(".tar")[0]

    if not path.exists(tarball):
        download(url, tarball)

    if not path.exists(path.join(build_dir, tarball_dir, "CMakeLists.txt")):
        hasher = hashlib.sha256()
        with open(tarball, "rb") as tb:
            hasher.update(tb.read())
        assert hasher.hexdigest() == sha256_sum

        with tarfile.open(tarball, "r:xz") as tb:
            tb.extractall(build_dir)


distutils.dir_util.mkpath(build_dir)
distutils.dir_util.mkpath(prefix_dir)
distutils.dir_util.mkpath(build_dir_ft)
distutils.dir_util.mkpath(build_dir_hb)

ensure_downloaded(FREETYPE_URL, FREETYPE_SHA256)
ensure_downloaded(HARFBUZZ_URL, HARFBUZZ_SHA256)

print("# First, build FreeType without Harfbuzz support")
shell(
    "cmake -DBUILD_SHARED_LIBS=OFF "
    "-DCMAKE_DISABLE_FIND_PACKAGE_HarfBuzz=TRUE -DFT_WITH_HARFBUZZ=OFF "
    "-DCMAKE_DISABLE_FIND_PACKAGE_PNG=TRUE "
    "-DCMAKE_DISABLE_FIND_PACKAGE_BZip2=TRUE "
    "-DCMAKE_DISABLE_FIND_PACKAGE_ZLIB=TRUE "
    "-DCMAKE_DISABLE_FIND_PACKAGE_BrotliDec=TRUE "
    "{} ..".format(CMAKE_GLOBAL_SWITCHES),
    cwd=build_dir_ft,
)
shell("cmake --build . --config Release --target install --parallel", cwd=build_dir_ft)

print("\n# Next, build Harfbuzz and point it to the FreeType we just build.")
shell(
    "cmake -DBUILD_SHARED_LIBS=OFF " +
    # https://stackoverflow.com/questions/3961446
    ("-DCMAKE_POSITION_INDEPENDENT_CODE=ON " if bitness > 32 else "")
    + "-DHB_HAVE_FREETYPE=ON -DHB_HAVE_GLIB=OFF -DHB_HAVE_CORETEXT=OFF "
    "{} ..".format(CMAKE_GLOBAL_SWITCHES),
    cwd=build_dir_hb,
)
shell("cmake --build . --config Release --target install --parallel", cwd=build_dir_hb)

print("\n# Lastly, rebuild FreeType, this time with Harfbuzz support.")
harfbuzz_includes = path.join(prefix_dir, "include", "harfbuzz")
shell(
    "cmake -DBUILD_SHARED_LIBS=ON "
    "-DCMAKE_DISABLE_FIND_PACKAGE_HarfBuzz=FALSE -DFT_WITH_HARFBUZZ=ON "
    "-DCMAKE_DISABLE_FIND_PACKAGE_PNG=TRUE "
    "-DCMAKE_DISABLE_FIND_PACKAGE_BZip2=TRUE "
    "-DCMAKE_DISABLE_FIND_PACKAGE_ZLIB=TRUE "
    "-DCMAKE_DISABLE_FIND_PACKAGE_BrotliDec=TRUE "
    '-DPKG_CONFIG_EXECUTABLE="" '  # Prevent finding system libraries
    '-DHARFBUZZ_INCLUDE_DIRS="{}" '
    "-DSKIP_INSTALL_HEADERS=ON "
    "{} ..".format(harfbuzz_includes, CMAKE_GLOBAL_SWITCHES),
    cwd=build_dir_ft,
)
shell("cmake --build . --config Release --target install --parallel", cwd=build_dir_ft)

# Move libraries from PREFIX/bin to PREFIX/lib if need be (Windows DLLs are
# treated as runtimes and may end up in bin/). This keeps setup.py simple.
target_dir = path.join(prefix_dir, "lib")
bin_so = glob.glob(path.join(prefix_dir, "bin", "*freetype*"))
bin_so.extend(glob.glob(path.join(prefix_dir, "lib64", "*freetype*")))
bin_so.extend(glob.glob(path.join(prefix_dir, "lib", "freetype*.dll")))
for so in bin_so:
    so_target_name = path.basename(so)
    if not so_target_name.startswith("lib"):
        so_target_name = "lib" + so_target_name
    lib_path = path.join(target_dir, so_target_name)

    print("# Moving '{}' to '{}'".format(so, lib_path))
    if not path.exists(target_dir):
        os.makedirs(target_dir)
    os.replace(so, lib_path)
