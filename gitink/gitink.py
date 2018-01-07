def get_dim(x_min, x_max, y_min, y_max):
    from collections import namedtuple

    Dimensions = namedtuple('Dimensions',
                            ['x_min',
                             'x_max',
                             'y_min',
                             'y_max'])

    dim = Dimensions(x_min, x_max, y_min, y_max)

    return dim


class Line:

    def __init__(self, b1, b2, ghost=False):

        x1, y1 = b1.get_center()
        x2, y2 = b2.get_center()

        self.ghost = ghost

        nsteps = 1000

        # find start
        for i in range(nsteps):
            u = x1 + i * (x2 - x1) / nsteps
            v = y1 + i * (y2 - y1) / nsteps
            if not b1.point_in_box(u, v):
                self.x1 = u
                self.y1 = v
                break

        # find end
        for i in range(nsteps):
            u = x2 + i * (x1 - x2) / nsteps
            v = y2 + i * (y1 - y2) / nsteps
            if not b2.point_in_box(u, v):
                self.x2 = u
                self.y2 = v
                break

    def svg(self, scaling, x_off, y_off):

        if self.ghost:
            opacity = 0.3
        else:
            opacity = 1.0

        return '<line x1="{0}" y1="{1}" x2="{2}" y2="{3}" style="stroke:#000000; stroke-width:{4}; stroke-opacity:{5}" />'.format(x_off + self.x1,
                                                                                                                                  y_off + self.y1,
                                                                                                                                  x_off + self.x2,
                                                                                                                                  y_off + self.y2,
                                                                                                                                  scaling * 4.0,
                                                                                                                                  opacity)


class Arrow(Line):

    def svg(self, scaling, x_off, y_off):

        if self.ghost:
            opacity = 0.3
        else:
            opacity = 1.0

        s = []
        s.append('<g')
        s.append('   inkscape:label="Layer 1"')
        s.append('   inkscape:groupmode="layer"')
        s.append('   id="layer1">')
        s.append('  <path')
        s.append('     style="fill:none;stroke:#000000;stroke-width:%f;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:%f;marker-end:url(#Arrow2Mend);stroke-miterlimit:4;stroke-dasharray:none"' % (scaling * 4.0, opacity))
        s.append('     d="M %f,%f %f,%f"' % (x_off + self.x1, y_off + self.y1, x_off + self.x2, y_off + self.y2))
        s.append('     id="path2985"')
        s.append('     inkscape:connector-curvature="0" />')
        s.append('</g>')

        return '\n'.join(s)


class Box:

    def __init__(self, dim, scaling, text, x, y, color, rounded=False, ghost=False):

        self.text = text
        self.color = color
        self.rounded = rounded
        self.ghost = ghost

        self.center = (x, y)

        self.box_w = 24.0 * len(text) + 20.0
        self.box_h = 58.0

        self.box_w *= scaling
        self.box_h *= scaling

        self.box_x = x - 0.5 * self.box_w
        self.box_y = y - 0.5 * self.box_h

        self.text_x = self.box_x + 10.0 * scaling
        self.text_y = self.box_y + 42.0 * scaling

    def update_dim(self, dim):
        x_min_loc = self.box_x
        y_min_loc = self.box_y
        x_max_loc = self.box_x + 2.0 * self.box_w
        y_max_loc = self.box_y + 2.0 * self.box_h

        x_min_loc = min(x_min_loc, dim.x_min)
        x_max_loc = max(x_max_loc, dim.x_max)
        y_min_loc = min(y_min_loc, dim.y_min)
        y_max_loc = max(y_max_loc, dim.y_max)

        return get_dim(x_min_loc, x_max_loc, y_min_loc, y_max_loc)

    def get_center(self):
        return self.center

    def point_in_box(self, x, y):

        x1 = self.center[0] - 0.5 * self.box_w
        x2 = self.center[0] + 0.5 * self.box_w

        y1 = self.center[1] - 0.5 * self.box_h
        y2 = self.center[1] + 0.5 * self.box_h

        if x < x1:
            return False
        if x > x2:
            return False
        if y < y1:
            return False
        if y > y2:
            return False

        return True

    def svg(self, scaling, x_off, y_off):

        if self.ghost:
            opacity = 0.3
            stroke_color = '#dddddd'
        else:
            opacity = 1.0
            stroke_color = '#000000'

        s = []

        s.append('<g')
        s.append('   inkscape:label="Layer 1"')
        s.append('   inkscape:groupmode="layer"')
        s.append('   id="layer1">')
        s.append('  <rect')
        s.append('     style="fill:%s;stroke:%s;stroke-width:%f;stroke-miterlimit:4;stroke-dasharray:none"' % (self.color, stroke_color, scaling * 4.0))
        s.append('     id="rect2989"')
        s.append('     width="%f"' % self.box_w)
        s.append('     height="%f"' % self.box_h)
        s.append('     x="%f"' % (x_off + self.box_x))
        s.append('     y="%f"' % (y_off + self.box_y))
        if self.rounded:
            s.append('     ry="%f" />' % (scaling * 8.0))
        else:
            s.append('     ry="%f" />' % 0.0)
        s.append('  <text')
        s.append('     xml:space="preserve"')
        s.append('     style="font-size:%ipx;font-style:normal;font-weight:normal;line-height:125%%;letter-spacing:0px;word-spacing:0px;fill:#000000;fill-opacity:%f;stroke:none;font-family:DejaVu Sans Mono"' % (int(scaling * 40), opacity))
        s.append('     x="%f"' % (x_off + self.text_x))
        s.append('     y="%f"' % (y_off + self.text_y))
        s.append('     id="text2985"')
        s.append('     sodipodi:linespacing="125%"><tspan')
        s.append('       sodipodi:role="line"')
        s.append('       id="tspan2987"')
        s.append('       x="%f"' % (x_off + self.text_x))
        s.append('       y="%f">%s</tspan></text>' % (y_off + self.text_y, self.text))
        s.append('</g>')

        return '\n'.join(s)


def print_head(w, h):

    s = []

    s.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    s.append('<!-- Created with GitInk -->')
    s.append('<svg')
    s.append('   xmlns:dc="http://purl.org/dc/elements/1.1/"')
    s.append('   xmlns:cc="http://creativecommons.org/ns#"')
    s.append('   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"')
    s.append('   xmlns:svg="http://www.w3.org/2000/svg"')
    s.append('   xmlns="http://www.w3.org/2000/svg"')
    s.append('   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"')
    s.append('   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"')
    s.append('   width="%f"' % w)
    s.append('   height="%f"' % h)
    s.append('   id="svg2"')
    s.append('   version="1.1"')
    s.append('   inkscape:version="0.48.3.1 r9886"')
    s.append('   sodipodi:docname="drawing.svg">')

    s.append('<defs')
    s.append('   id="defs4">')
    s.append('  <marker')
    s.append('     inkscape:stockid="Arrow2Mend"')
    s.append('     orient="auto"')
    s.append('     refY="0.0"')
    s.append('     refX="0.0"')
    s.append('     id="Arrow2Mend"')
    s.append('     style="overflow:visible;">')
    s.append('    <path')
    s.append('       id="path3786"')
    s.append('       style="fill-rule:evenodd;stroke-width:0.62500000;stroke-linejoin:round;"')
    s.append('       d="M 8.7185878,4.0337352 L -2.2072895,0.016013256 L 8.7185884,-4.0017078 C 6.9730900,-1.6296469 6.9831476,1.6157441 8.7185878,4.0337352 z "')
    s.append('       transform="scale(0.6) rotate(180) translate(0,0)" />')
    s.append('  </marker>')
    s.append('</defs>')

    return '\n'.join(s)


def pointer(dim, scaling, b, text, position):

    assert position in ['above', 'below']

    if position == 'above':
        sign = +1.0
    elif position == 'below':
        sign = -1.0

    x, y = b.get_center()

    if text[0] == '_':
        p = Box(dim, scaling, text[1:], x, y - sign * 100.0 * scaling, '#ffffff', ghost=True)
        a = Arrow(p, b, ghost=True)
    else:
        p = Box(dim, scaling, text, x, y - sign * 100.0 * scaling, '#dddddd')
        a = Arrow(p, b)

    dim = p.update_dim(dim)

    return p, a, dim


def commit(dim, scaling, text, row, parents=[]):

    color = []

    # FIXME
    color.append('#ff9999')
    color.append('#99ff99')
    color.append('#9999ff')
    color.append('#ff9999')
    color.append('#99ff99')
    color.append('#9999ff')
    color.append('#ff9999')
    color.append('#99ff99')
    color.append('#9999ff')
    color.append('#ff9999')
    color.append('#99ff99')
    color.append('#9999ff')

    origin = [50.0, 50.0]

    x, y = origin

    y += row * 50.0 * scaling

    for p in parents:
        p_x, p_y = p.get_center()
        t = p_x + 150.0 * scaling
        if t > x:
            x = t

    c = Box(dim, scaling, text, x, y, color[row], rounded=True)
    dim = c.update_dim(dim)

    arrows = []
    for p in parents:
        # a = Arrow(c, p)  # students find the arrow pointing backwards confusing
        a = Line(c, p)
        arrows.append(a)

    return c, arrows, dim


def print_svg(dim, scaling, history):
    import re
    from .extract_characters import get_safe_character

    history = history.split('\n')

    # get dimensions of text in order to estimate svg dimensions
    history_y = len(history)
    history_x = 0
    for line in history:
        if len(line) > history_x:
            history_x = len(line)

    # get the time order of commits and "coordinates" of commits
    commits_time_order = []
    commit_coor = {}
    coor_commit = {}
    row = 0
    for line in history:
        # we ignore branch pointers here
        for w in re.findall(r'\w+[*]?', re.sub(r"\[.*\]", '', line)):
            i = line.find(w)
            j = i + len(w) - 1
            commits_time_order.append((i, w))
            commit_coor[w] = (row, i, j)
            coor_commit[(row, j)] = w
        row += 1
    commits_time_order.sort()

    # get coordinates of possible branch names
    coor_pointer = {}
    row = 0
    for line in history:
        # we specifically look for branch names "[branch]"
        for w in re.findall(r'\[(.*?)\]', line):
            i = line.rfind(w)
            coor_pointer[(row, i)] = w
        row += 1

    # figure out the parents of commits
    parents = {}
    for c in commit_coor:
        parents[c] = []
        row, i, j = commit_coor[c]
        # left parent
        if get_safe_character(history, row, i - 1) == '-':
            parents[c].append(re.findall('\w+[*]?', history[row].split(c)[0])[-1])
        # top parent
        if get_safe_character(history, row - 1, i - 1) == '\\':
            parents[c].append(coor_commit[(row - 2, i - 2)])
        # bottom parent
        if get_safe_character(history, row + 1, i - 1) == '/':
            parents[c].append(coor_commit[(row + 2, i - 2)])

    # figure out possible branch names that point to commits
    pointers = {}
    for c in commit_coor:
        pointers[c] = []
        row, i, j = commit_coor[c]
        # pointers above
        if get_safe_character(history, row - 1, i) == '|':
            pointers[c].append((coor_pointer[(row - 2, i)], 'above'))
        # pointers below
        if get_safe_character(history, row + 1, i) == '|':
            pointers[c].append((coor_pointer[(row + 2, i)], 'below'))

    c_dict = {}
    all_objects = []
    for i, c in commits_time_order:
        row = commit_coor[c][0]
        if parents[c] == []:
            c_dict[c], arrows, dim = commit(dim, scaling, c, row)
        else:
            p = []
            for parent in parents[c]:
                p.append(c_dict[parent])
            c_dict[c], arrows, dim = commit(dim, scaling, c, row, p)
        all_objects.append(c_dict[c])
        for a in arrows:
            all_objects.append(a)
        for p in pointers[c]:
            t = []
            for j, w in enumerate(p[0].split(',')):
                if j == 0:
                    ptr, a, dim = pointer(dim, scaling, c_dict[c], w, p[1])
                else:
                    ptr, a, dim = pointer(dim, scaling, t[j - 1], w, p[1])
                t.append(ptr)
                all_objects.append(ptr)
                all_objects.append(a)

    s_svg = print_head(dim.x_max - dim.x_min, dim.y_max - dim.y_min)

    for o in all_objects:
        # the +5.0 so that the figure does not start directly at the origin
        # looks better with some offset
        s_svg += o.svg(scaling, -dim.x_min + 5.0, -dim.y_min + 5.0)

    s_svg += '</svg>'

    return s_svg


def main():
    from sys import float_info, argv

    # holds dimensions used for trimming the image
    m = float_info.max
    dim = get_dim(m, -m, m, -m)

    with open(argv[1], 'r') as f:
        s_svg = print_svg(dim=dim,
                          scaling=0.4,
                          history=f.read())
        print(s_svg)


if __name__ == '__main__':
    main()
