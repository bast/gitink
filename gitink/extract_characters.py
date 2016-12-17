def get_safe_character(s, row, i):

    # return ' ' if we ask for an invalid row
    if row not in range(len(s)):
        return ' '

    # return ' ' if we ask for an invalid character
    if i not in range(len(s[row])):
        return ' '

    return s[row][i]


def test_get_safe_character():

    text = ['abc', 'def', 'ghi']

    assert get_safe_character(text, 0, 1) == 'b'
    assert get_safe_character(text, 1, 0) == 'd'
    assert get_safe_character(text, -1, 0) == ' ', 'testing invalid row'
    assert get_safe_character(text, 3, 0) == ' ', 'testing invalid row'
    assert get_safe_character(text, 0, -1) == ' ', 'testing invalid character'
    assert get_safe_character(text, 0, 3) == ' ', 'testing invalid character'
