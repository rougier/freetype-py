import os

import freetype
import pytest

test_folder = os.path.realpath(os.path.dirname(__file__))

def _ft_ver():
    ft_ver_tuple = freetype.version()
    ft_ver_str = ".".join(['{}'.format(i) for i in ft_ver_tuple])

    return ft_ver_tuple, ft_ver_str


def test_variable_font_basics():
    """
    Check that basic VF functionality functions (open a VF font, get VF info)
    """
    ft_vt, ft_vs = _ft_ver()
    if ft_vt < (2, 8, 1):
        # note: there is some proto-VF (Multiple Master) support in older
        # FreeType versions, but not enough to work with here.
        pytest.skip("Incomplete VF support in FreeType lib {} (need 2.8.1 or later)".format(ft_vs))
        return

    font_path = os.path.join(
        test_folder,
        "..",
        "examples",
        "SourceSansVariable-Roman.otf")
    face = freetype.Face(font_path)
    var_info = face.get_variation_info()

    assert len(var_info.axes) == 1
    assert var_info.axes[0].tag == 'wght'

    assert len(var_info.instances) == 6
    for ii, cv in enumerate((200, 300, 400, 600, 700, 900)):
        assert var_info.instances[ii].coords == (cv,)


def test_vf_axis_get_set():
    ft_vt, ft_vs = _ft_ver()
    if ft_vt < (2, 8, 1):
        pytest.skip("Incomplete VF support in FreeType lib {} (need 2.8.1 or later)".format(ft_vs))
        return

    font_path = os.path.join(
        test_folder,
        "..",
        "examples",
        "SourceSansVariable-Roman.otf")

    face = freetype.Face(font_path)

    dc_in = (373,)
    face.set_var_design_coords(dc_in)
    dcoords = face.get_var_design_coords()
    assert dcoords[0] == dc_in[0]

    bc_in = (-0.5,)
    face.set_var_blend_coords(bc_in)
    bcoords = face.get_var_blend_coords()
    assert bcoords[0] == bc_in[0]

    # try 'reset to defaults' option
    face.set_var_design_coords(None, reset=True)
    dcoords = face.get_var_design_coords()
    vsi = face.get_variation_info()
    expected = tuple([vsi.axes[i].default for i in range(len(dcoords))])
    assert dcoords == expected


def test_vf_set_named_instance():
    ft_vt, ft_vs = _ft_ver()
    if ft_vt < (2, 8, 1):
        pytest.skip("Incomplete VF support in FreeType lib {} (need 2.8.1 or later)".format(ft_vs))
        return

    font_path = os.path.join(
        test_folder,
        "..",
        "examples",
        "SourceSansVariable-Roman.otf")

    face = freetype.Face(font_path)
    vsi = face.get_variation_info()

    for inst in vsi.instances:
        face.set_var_named_instance(inst.name)
        dcoords = face.get_var_design_coords()
        assert dcoords == inst.coords
