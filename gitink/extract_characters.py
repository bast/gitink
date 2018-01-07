def get_safe_character(text, row, i):

    # return None if we ask for an invalid row
    if row not in range(len(text)):
        return None

    # return None if we ask for an invalid position in a valid row
    if i not in range(len(text[row])):
        return None

    return text[row][i]


def test_get_safe_character():

    text = ['abc', 'def', 'ghi']

    assert get_safe_character(text, 0, 1) == 'b'
    assert get_safe_character(text, 1, 0) == 'd'
    assert get_safe_character(text, -1, 0) is None, 'testing invalid row'
    assert get_safe_character(text, 3, 0) is None, 'testing invalid row'
    assert get_safe_character(text, 0, -1) is None, 'testing position in a valid row'
    assert get_safe_character(text, 0, 3) is None, 'testing position in a valid row'
