#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import traceback

from typing import Dict

from fontTools.ttLib import TTFont

from ctypes import byref
from freetype import (
    FT_Done_Face,
    FT_Done_FreeType,
    FT_Exception,
    FT_Face,
    FT_Get_First_Char,
    FT_Get_Next_Char,
    FT_Init_FreeType,
    FT_Library,
    FT_New_Memory_Face,
    FT_UInt,
    FT_Get_Char_Index,
    FT_Face_GetVariantSelectors,
    FT_Face_GetCharsOfVariant,
    FT_Face_GetCharVariantIndex,
    FT_Face_GetCharVariantIsDefault
)

_ALL_IVS_NUMBERS  = [x for x in range( 0xe0100, 0xe01f0)] # Supplemental
_ALL_IVS_NUMBERS += [x for x in range( 0xfe00,  0xfe10)]  # IVS

def _read_cmap_uvs(uvsDict):
    global _ALL_IVS_NUMBERS

    all_characters         = {}
    all_default_characters = []
    for item, item_list in uvsDict.items():
        ivs_val = int(item)
        if ivs_val in _ALL_IVS_NUMBERS:
            ivs_chr = chr(ivs_val)
            for character_tuple in item_list:
                character_val = character_tuple[0]
                glyph_name    = character_tuple[1]
                if glyph_name:
                    if glyph_name == '.notdef':
                        continue

                    character     = chr(int(character_val))
                    ivs_character = character + ivs_chr
                    assert ivs_character not in all_characters
                    all_characters[ivs_character] = glyph_name
                else:
                    character     = chr(int(character_val))
                    ivs_character = character + ivs_chr
                    all_default_characters.append(ivs_character)

    return all_characters, all_default_characters

def _read_character(character_value, encoding):  
    if encoding == 'utf_16_be':
        character_string = chr(character_value)  
    else:
        return None

    return character_string

_CMAP_PRIORITY_LIST = [
    (3, 10),  # Windows Unicode full repertoire
    (0,  6),  # Unicode full repertoire (format 13 subtable)
    (0,  4),  # Unicode 2.0 full repertoire
    (3,  1),  # Windows Unicode BMP
    (0,  3),  # Unicode 2.0 BMP
    (0,  2),  # Unicode ISO/IEC 10646
    (0,  1),  # Unicode 1.1
    (0,  0)   # Unicode 1.0
]

def read_fonttools_cmap(font) -> Dict[str, str]:
    global _CMAP_PRIORITY_LIST

    assert isinstance(font, TTFont)
    if not hasattr(font["cmap"], 'tables'):
        return None

    all_characters         = {}
    all_default_characters = []
    best_read_index        = None
    all_tables             = font["cmap"].tables
    for table in all_tables:
        encoding        = table.getEncoding()
        if not encoding:
            continue
        if encoding != 'utf_16_be':
            continue       
        try:
            if table.format == 14:
                if hasattr(table, 'uvsDict'):
                    all_uvs_data, default_characters = _read_cmap_uvs(table.uvsDict)
                    all_default_characters          += default_characters
                    for character, glyphname in all_uvs_data.items():
                        if character in all_characters:
                            assert all_characters[character] == glyphname
                        else:
                            all_characters[character] = glyphname
                else:
                    print('Unknown CMAP Format 14: {}:'.format(vars(table)))

            elif hasattr(table, 'cmap'):
                tuple_value = (table.platformID, table.platEncID)
                if tuple_value in _CMAP_PRIORITY_LIST:
                    index_value = _CMAP_PRIORITY_LIST.index(tuple_value)
                    if best_read_index:
                        if index_value < best_read_index:
                            best_read_index = index_value
                        else:
                            continue
                    else:
                        best_read_index = index_value

                all_items = table.cmap.items()
                length = len(all_items)
                if length == 0:
                    if table.format != 6:
                        print('Unknown CMAP Format {}: {}:'.format(table.format, vars(table)))

                for item in all_items:
                    character = _read_character(item[0], encoding)
                    glyphname = item[1]
                    if glyphname == '.notdef':
                        continue

                    if character is not None:
                        if character in all_characters:
                            if all_characters[character] != glyphname:
                                all_characters[character] = glyphname
                        else:
                            all_characters[character] = glyphname

        except:
            traceback.print_exc()
            continue

    if all_default_characters:
        for ivs_character in all_default_characters:
            first_character = ivs_character[0]
            if first_character in all_characters:
                glyphname                     = all_characters[first_character]
                all_characters[ivs_character] = glyphname

    return all_characters

def read_freetype_cmap(face: FT_Face) -> Dict[str, int]:
    platID     = face.contents.charmap.contents.platform_id
    encodingID = face.contents.charmap.contents.encoding_id
    if platID == 3:
        if encodingID not in [1, 10]:
            return {}

    elif platID == 0: # all unicode
        pass

    else: # everything else
        return {}

    all_characters = []
    gindex         = FT_UInt()
    charcode       = FT_Get_First_Char( face, byref(gindex) )
    while gindex.value != 0:
        character = chr(charcode)
        all_characters.append(character)
        charcode = FT_Get_Next_Char( face, charcode, byref(gindex) )

    variant_selectors_list = FT_Face_GetVariantSelectors(face)
    if bool(variant_selectors_list):
        all_selectors  = []
        selector_value = variant_selectors_list[0]
        index          = 0

        while selector_value != 0:
            all_selectors.append(selector_value)

            index         += 1
            selector_value = variant_selectors_list[index]

        for selector_value in all_selectors:
            character_value_list = FT_Face_GetCharsOfVariant(face, selector_value)
            assert(bool(character_value_list))
            character_value = character_value_list[0]
            index           = 0

            while character_value != 0:
                character = chr(character_value) + chr(selector_value)
                all_characters.append(character)

                index          += 1
                character_value = character_value_list[index]

    character_to_glyphID = {}
    for character in all_characters:
        if len(character) == 2:
            character_value = ord(character[0])
            selector_value  = ord(character[1])
            glyphID         = FT_Face_GetCharVariantIndex(face, character_value, selector_value)
            if glyphID != 0:
                assert character not in character_to_glyphID
                character_to_glyphID[character] = glyphID
        else:
            assert len(character) == 1
            character_value = ord(character)
            glyphID         = FT_Get_Char_Index(face, character_value)
            if glyphID != 0:
                assert character not in character_to_glyphID
                character_to_glyphID[character] = glyphID

    return character_to_glyphID

def _convert_character_to_hex(text: str):
    assert len(text) == 1
    value = ord(text)
    if 0x0000 <= value <= 0xFFFF:
        assert len(hex(value)) <= 6
        return '{0:04x}'.format(value)
    elif value <= 0xFFFFF:
        assert len(hex(value)) <= 7
        return '{0:05x}'.format(value)
    elif value <= 0xFFFFFF:
        assert len(hex(value)) <= 8
        return '{0:06x}'.format(value)
    elif value <= 0xFFFFFFF:
        assert len(hex(value)) <= 9
        return '{0:07x}'.format(value)
    elif value <= 0xFFFFFFFF:
        assert len(hex(value)) <= 9
        return '{0:08x}'.format(value)
    else:
        raise RuntimeError()

def convert_string_to_hex(text: str):
    assert isinstance(text, str)
    result = ''
    for count, character in enumerate(text):
        if count > 0:
            result += '-{}'.format(_convert_character_to_hex(character))
        else:
            result += '{}'.format(_convert_character_to_hex(character))

    return result

if __name__ == "__main__":
    directory   = os.path.dirname(__file__)
    font_path   = os.path.join(directory, 'SourceHanSans-Regular.ttc')
    memory_file = io.BytesIO()
    with open(font_path, 'rb') as fontfile:
        memory_file.write(fontfile.read())
        memory_file.seek(0)
    
    fonttools_font = TTFont(memory_file, 0, allowVID=0,
                            ignoreDecompileErrors=True,
                            fontNumber=0)

    library = FT_Library()
    error   = FT_Init_FreeType(byref(library))
    if error: raise FT_Exception(error)

    freetype_face = FT_Face()
    data          = memory_file.getvalue()
    error         = FT_New_Memory_Face(library, data, len(data), 0, byref(freetype_face))
    if error: raise FT_Exception(error)

    all_freetype_characters  = read_freetype_cmap(freetype_face)
    all_fonttools_characters = read_fonttools_cmap(fonttools_font)

    print('Read {} Free Type Characters'.format(len(all_freetype_characters)))
    print('Read {} Font Tools Characters'.format(len(all_fonttools_characters)))

    print('Checking Mapping')

    for character, glyphID in all_freetype_characters.items():
        glyphname = fonttools_font.getGlyphName(glyphID)
        if character in all_fonttools_characters:
            ft_glyphname = all_fonttools_characters[character]
            if ft_glyphname != glyphname:
                character_hex = convert_string_to_hex(character)
                print('Glyph Mismatch: {} Free Type: {} Font Tools: {}'.format(character_hex, glyphname, ft_glyphname))

        else:
            character_hex = convert_string_to_hex(character)
            print('Glyph Missing in Font Tools: {}'.format(character_hex))

    for character, glyphname in all_fonttools_characters.items():
        if character in all_freetype_characters:
            ft_glyphID   = all_freetype_characters[character]
            ft_glyphname = fonttools_font.getGlyphName(ft_glyphID)
            if ft_glyphname != glyphname:
                character_hex = convert_string_to_hex(character)
                print('Glyph Mismatch: {} Font Tools: {} Free Type: {}'.format(character_hex, glyphname, ft_glyphname))

        else:
            character_hex = convert_string_to_hex(character)
            print('Glyph Missing in Free Type: {}'.format(character_hex))

    print('Finished Checking Mapping')

    FT_Done_Face(freetype_face)
    FT_Done_FreeType(library)
