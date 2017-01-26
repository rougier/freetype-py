import ctypes as ct

import os
import platform
import ctypes.util
import warnings

from freetype.ft_structs import FT_Library
from freetype.ft_types import FT_Int

# on windows all ctypes does when checking for the library
# is to append .dll to the end and look for an exact match
# within any entry in PATH.
filename = ct.util.find_library('freetype')

osName = platform.system()

if filename is None:
    if osName == 'Windows':
        # Check current working directory for dll as ctypes fails to do so
        filename = os.path.join(os.path.realpath('.'), 'freetype.dll')
    else:
        filename = 'libfreetype.so.6'

try:
    _lib = ct.CDLL(filename)
except (OSError, TypeError):
    _lib = None
    raise RuntimeError('Freetype library not found')


if osName == 'Windows':
    _funcType = ct.WINFUNCTYPE
else: # Linux and OS X
    _funcType = ct.CFUNCTYPE

_version = None


# functions needed to do version checking on the freetype library.
FT_Init_FreeType   = _lib.FT_Init_FreeType
FT_Done_FreeType   = _lib.FT_Done_FreeType
FT_Library_Version = _lib.FT_Library_Version

def _get_ft_version():

    handle = FT_Library()
    FT_Init_FreeType(ct.byref(handle))
    major = FT_Int(0)
    minor = FT_Int(0)
    patch = FT_Int(0)

    FT_Library_Version(handle, ct.byref(major), ct.byref(minor), ct.byref(patch))

    FT_Done_FreeType(handle)

    return (major.value, minor.value, patch.value)

class _FTUndefinedFunction(object):
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __call__(self, *args, **kwargs):
        reqStr = '.'.join(map(str, self.version))
        verStr = '.'.join(map(str, _version))

        message = 'The function {0} is not implemented in Freetype {1}' \
                ', Freetype {2} or above is required.'.format(self.name,
                verStr, reqStr)

        warnings.simplefilter("always")
        warnings.warn(message)
        warnings.simplefilter("default")

def _ft_func(name, returnType, paramTypes, version=None):
    '''
    Define function for the freetype library

    Version requirements can be set on functions which will
    emit a warning for older freetype versions.
    '''
    global _version

    if version is not None:
        if _version is None:
            _version = _get_ft_version()

        if not _version >= version:
            verStr = '.'.join(map(str, _version))

            message = 'FreeType {} installed, newer functionallity will ' \
                    'not be available.'.format(verStr)

            warnings.warn(message)
            return _FTUndefinedFunction(name, version)

    try:
        address = getattr(_lib, name)
        function = _funcType(returnType, *paramTypes)

    except AttributeError:
        raise AttributeError('{}: Function not found.'.format(name))

    return ct.cast(address, function)


class EnumTypeBase(object):
    def __init__(self, name, value):
        self._name = name
        self._value = value

        self._as_parameter_ = ct.c_int(self.value)

    @property
    def value(self):
        return self._value

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @classmethod
    def from_param(cls, obj):
        try:
            if obj.type == cls._type:
                return obj._as_parameter_
            else:
                raise TypeError('Incorrect enum type.')
        except AttributeError:
            if not isinstance(obj, EnumWrapper) and obj.type != self.type:
                raise TypeError('Incorrect type.')
            else:
                raise

class Enum(object):

    def __init__(self, enumType, enums):

        self.type = enumType

        self.enums = {}

        enumCounter = 0

        EnumClass = type(enumType, (EnumTypeBase,), {'_type': enumType})

        for i, enum in enumerate(enums):
            enumSplit = enum.split('=')

            splitNum = len(enumSplit)

            if splitNum == 2:
                enumCounter = int(enumSplit[1])

            elif splitNum > 2:
                raise SyntaxError('Enum {0} Incorrect enum syntax.'.format(i+1))
            
            else:
                enumCounter += 1

            self.enums[enumSplit[0]] = EnumClass(enumSplit[0], enumCounter)

        self.enums[self.type] = EnumClass

        globals().update(self.enums)