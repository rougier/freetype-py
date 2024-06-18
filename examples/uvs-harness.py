#!/usr/bin/env python
# -*- coding: utf-8 -*-

# shorter Unicode Variation Sequences example from #195, with comparison to hb-shape.

# The test file used and known to work is v2.004 of https://github.com/adobe-fonts/source-han-sans/blob/release/OTF/Japanese/SourceHanSans-Regular.otf

import importlib
uvs = importlib.import_module("unicode-variation-sequences")

read_freetype_cmap = uvs.read_freetype_cmap

if __name__ == "__main__":
    import os, io
    directory   = os.path.dirname(__file__)
    font_path   = os.path.join(directory, 'SourceHanSans-Regular.otf')
    memory_file = io.BytesIO()
    with open(font_path, 'rb') as fontfile:
        memory_file.write(fontfile.read())
        memory_file.seek(0)
    
    from freetype import *
    library = FT_Library()
    error   = FT_Init_FreeType(byref(library))
    if error: raise FT_Exception(error)

    freetype_face = FT_Face()
    data          = memory_file.getvalue()
    error         = FT_New_Memory_Face(library, data, len(data), 0, byref(freetype_face))
    if error: raise FT_Exception(error)

    all_freetype_characters  = read_freetype_cmap(freetype_face)
    # {'邉' : ['邉󠄁', '邉󠄂', '邉󠄃', '邉󠄄', '邉󠄅', '邉󠄆', '邉󠄇', '邉󠄈', '邉󠄉', '邉󠄊', '邉󠄋', '邉󠄌', '邉󠄍', '邉󠄎', '邉󠄀']}
    
    print(all_freetype_characters['邉'], all_freetype_characters['邉󠄁'], all_freetype_characters['邉󠄂'], all_freetype_characters['邉󠄃'], 
          all_freetype_characters['邉󠄄'], all_freetype_characters['邉󠄅'], all_freetype_characters['邉󠄆'], all_freetype_characters['邉󠄇'],
          all_freetype_characters['邉󠄈'], all_freetype_characters['邉󠄉'], all_freetype_characters['邉󠄊'], all_freetype_characters['邉󠄋'],
          all_freetype_characters['邉󠄌'], all_freetype_characters['邉󠄍'], all_freetype_characters['邉󠄎'], all_freetype_characters['邉󠄀'],
          sep='|')
    print('The above should be identical to the output of this hb-shape command:')
    print('    hb-shape --no-glyph-names --no-positions --no-clusters --no-advances SourceHanSans-Regular.otf "邉邉󠄁邉󠄂邉󠄃邉󠄄邉󠄅邉󠄆邉󠄇邉󠄈邉󠄉邉󠄊邉󠄋邉󠄌邉󠄍邉󠄎邉󠄀"')
