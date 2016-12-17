def get_safe_character(text, row, i):

    # return ' ' if we ask for an invalid row
    if row not in range(len(text)):
        return ' '

    # return ' ' if we ask for an invalid position in a valid row
    if i not in range(len(text[row])):
        return ' '

    return text[row][i]


def test_get_safe_character():

    text = ['abc', 'def', 'ghi']

    assert get_safe_character(text, 0, 1) == 'b'
    assert get_safe_character(text, 1, 0) == 'd'
    assert get_safe_character(text, -1, 0) == ' ', 'testing invalid row'
    assert get_safe_character(text, 3, 0) == ' ', 'testing invalid row'
    assert get_safe_character(text, 0, -1) == ' ', 'testing position in a valid row'
    assert get_safe_character(text, 0, 3) == ' ', 'testing position in a valid row'
