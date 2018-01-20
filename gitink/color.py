def get_color(text):
    if text.startswith('a'):
        return '#ff0000', '#ffaaaa'
    if text.startswith('b'):
        return '#00ff00', '#aaffaa'
    if text.startswith('c'):
        return '#0000ff', '#aaaaff'
    if text.startswith('e'):
        return '#000000', '#aaaaaa'
    if text.startswith('m'):
        return '#000000', '#aaaaaa'
    return '#ff0000', '#ffaaaa'
