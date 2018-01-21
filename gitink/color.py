def whiter_shade_of_pale(hex_color):
    '''
    This function pales the color a bit for the interior
    of the boxes.
    '''
    pale_shift = 70

    # separate the red, green, blue parts
    r_hex = hex_color[1:3]
    g_hex = hex_color[3:5]
    b_hex = hex_color[5:7]

    # convert from hex to dec
    r_dec = int(r_hex, 16)
    g_dec = int(g_hex, 16)
    b_dec = int(b_hex, 16)

    # make the color paler but make sure we do not go
    # beyond 255 or ff
    r_dec = min(255, r_dec + pale_shift)
    g_dec = min(255, g_dec + pale_shift)
    b_dec = min(255, b_dec + pale_shift)

    # convert from dec to hex
    r_hex = format(r_dec, '02x')
    g_hex = format(g_dec, '02x')
    b_hex = format(b_dec, '02x')

    # stitch them again together
    return '#{0}{1}{2}'.format(r_hex, g_hex, b_hex)


def get_color(text):

    # this is the deep palette of https://seaborn.pydata.org/
    palette = ['#4C72B0',
               '#55A868',
               '#C44E52',
               '#8172B2',
               '#CCB974',
               '#64B5CD']

    position = ord(text[0]) % len(palette)
    color = palette[position]
    pale_color = whiter_shade_of_pale(color)

    return color, pale_color
