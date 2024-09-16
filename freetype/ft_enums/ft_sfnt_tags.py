FT_SFNT_TAGS = {
    'FT_SFNT_HEAD'  : 0,
    'FT_SFNT_MAXP'  : 1,
    'FT_SFNT_OS2'   : 2,
    'FT_SFNT_HHEA'  : 3,
    'FT_SFNT_VHEA'  : 4,
    'FT_SFNT_POST'  : 5,
    'FT_SFNT_PCLT'  : 6,
}
FT_SFNT_MAX = len(FT_SFNT_TAGS)
# get value from dict indirectly to avoid complains from static checkers
ft_sfnt_head = FT_SFNT_TAGS['FT_SFNT_HEAD']
ft_sfnt_maxp = FT_SFNT_TAGS['FT_SFNT_MAXP']
ft_sfnt_os2 = FT_SFNT_TAGS['FT_SFNT_OS2']
ft_sfnt_hhea = FT_SFNT_TAGS['FT_SFNT_HHEA']
ft_sfnt_vhea = FT_SFNT_TAGS['FT_SFNT_VHEA']
ft_sfnt_post = FT_SFNT_TAGS['FT_SFNT_POST']
ft_sfnt_pclt = FT_SFNT_TAGS['FT_SFNT_PCLT']
globals().update(FT_SFNT_TAGS)