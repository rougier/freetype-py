"""Custom PEP 517 build backend to provide different dependencies for wheel builds.

We need some extra dependencies when we build a wheel that bundles the FreeType
shared library (triggered when FREETYPEPY_BUNDLE_FT environment variable is set),
as opposed to a pure Python wheel (py3-none-any.whl).

For more info see:

https://setuptools.pypa.io/en/latest/build_meta.html#dynamic-build-dependencies-and-other-build-meta-tweaks

https://github.com/rougier/freetype-py/issues/183
"""

import os
from setuptools import build_meta as _orig
from setuptools.build_meta import *


def get_requires_for_build_wheel(config_settings=None):
    build_wheel_deps = _orig.get_requires_for_build_wheel(config_settings)

    if os.environ.get("FREETYPEPY_BUNDLE_FT"):
        build_wheel_deps += ["certifi", "cmake"]

    return build_wheel_deps


def get_requires_for_build_editable(config_settings=None):
    # ensure pip install -e . uses same build deps as regular pip install/wheel
    return get_requires_for_build_wheel(config_settings)
