import sys
import re
from collections import namedtuple
from ascii2graph import graph
from .color import get_color
from .svg import draw_box, draw_line, draw_arrow, embed_svg, get_box_dims


def get_box_center(scale, text, origin):
    (x, y) = origin
    width, height = get_box_dims(scale, text)
    return x + 0.5 * width, y + 0.5 * height


def parse_graph(file_name):
    with open(file_name, 'r') as f:
        text = f.read()
        return graph(text)


def move_children_behind_current_commit(scale,
                                        time_direction,
                                        min_separation,
                                        commit,
                                        commits,
                                        placement):

    (_, _, text) = commit
    width, height = get_box_dims(scale, text)

    if time_direction in [90, 270]:
        _time_dim = 0
        _sep_dim = 1
    else:
        _time_dim = 1
        _sep_dim = 0

    children = commits[commit]
    for child in children:
        (line_number, character_position, text, angle) = child
        k = (line_number, character_position, text)

        # in our definition the angle difference cannot be larger than 90
        # unless the time_direction is 0
        if abs(angle - time_direction) > 90:
            angle -= 360

        # time direction | smaller | larger
        # 0              | left    | right
        # 90             | up      | down
        # 180            | right   | left
        # 270            | down    | up
        if time_direction in [0, 90]:
            if (angle - time_direction) < 0:
                shift = 'min'
            elif (angle - time_direction) > 0:
                shift = 'max'
            else:
                shift = None
        else:
            if (angle - time_direction) < 0:
                shift = 'max'
            elif (angle - time_direction) > 0:
                shift = 'min'
            else:
                shift = None
        if shift == 'min':
            placement[k][_sep_dim] = min(placement[k][_sep_dim], placement[commit][_sep_dim] - min_separation)
        elif shift == 'max':
            placement[k][_sep_dim] = max(placement[k][_sep_dim], placement[commit][_sep_dim] + min_separation)
        else:
            placement[k][_sep_dim] = placement[commit][_sep_dim]

        # displace children in the direction of the time arrow
        # make sure children are placed behind parents
        if time_direction in [90, 180]:
            placement[k][_time_dim] = max(placement[k][_time_dim], placement[commit][_time_dim] + min_separation)
        else:
            placement[k][_time_dim] = min(placement[k][_time_dim], placement[commit][_time_dim] - min_separation)

        placement = move_children_behind_current_commit(scale,
                                                        time_direction,
                                                        min_separation,
                                                        k,
                                                        commits,
                                                        placement)
    return placement


def point_inside_box(point_xy,
                     box_center_xy,
                     box_width,
                     box_height):
    if point_xy[0] > box_center_xy[0] + 0.5 * box_width:
        return False
    if point_xy[0] < box_center_xy[0] - 0.5 * box_width:
        return False
    if point_xy[1] > box_center_xy[1] + 0.5 * box_height:
        return False
    if point_xy[1] < box_center_xy[1] - 0.5 * box_height:
        return False
    return True


def arrow_head(arrow_origin_xy,
               box_center_xy,
               box_width,
               box_height):
    '''
    Locates the arrow head so that it is just barely outside the target box.
    '''
    vx = arrow_origin_xy[0] - box_center_xy[0]
    vy = arrow_origin_xy[1] - box_center_xy[1]

    # this is done in a silly way
    num_steps = 100
    for f in range(num_steps + 1):
        s = f / num_steps
        x = box_center_xy[0] + s * vx
        y = box_center_xy[1] + s * vy
        if not point_inside_box((x, y),
                                box_center_xy,
                                box_width,
                                box_height):
            return x, y
    sys.stderr.write('ERROR: head not found in arrow_head\n')
    sys.exit(1)


def main(scale, in_file, time_direction):
    assert time_direction in [0, 90, 180, 270]

    if time_direction == 0:
        forward_angles = [315, 0, 45]
    elif time_direction == 90:
        forward_angles = [45, 90, 135]
    elif time_direction == 180:
        forward_angles = [135, 180, 225]
    elif time_direction == 270:
        forward_angles = [225, 270, 315]

    file_name = in_file
    _graph = parse_graph(file_name)

    # filter out all branches and tags
    _commits = {node: _graph[node] for node in _graph if not node[2].startswith('[')}

    # only keep pointers (branches, tags)
    pointers = {node: _graph[node] for node in _graph if node[2].startswith('[')}

    # make sure edges point to children only
    # we do this by filtering out all angles that point "backwards"
    commits = {}
    for node in _commits:
        commits[node] = []
    for node in _commits:
        for child in _commits[node]:
            angle = child[3]
            if angle in forward_angles:
                commits[node].append(child)

    parents = {}
    for node in commits:
        for child in commits[node]:
            (line_number, character_position, text, _) = child
            k = (line_number, character_position, text)
            if k not in parents:
                parents[k] = []
            parents[k].append(node)

    # find root commit, this is the commit without any parents
    commits_without_parents = [commit for commit in commits if commit not in parents]
    assert len(commits_without_parents) == 1
    root_commit = commits_without_parents[0]

    placement = {}
    for (line_number, character_position, name) in commits:
        placement[(line_number, character_position, name)] = [0.0, 0.0]

    placement = move_children_behind_current_commit(scale=scale,
                                                    time_direction=time_direction,
                                                    min_separation=scale * 60.0,
                                                    commit=root_commit,
                                                    commits=commits,
                                                    placement=placement)

    s_svg = ''

    # first we place the edges
    for node in commits:
        center_parent = get_box_center(scale, name, placement[node])
        for child in commits[node]:
            (line_number, character_position, text, _) = child
            k = (line_number, character_position, text)
            center_child = get_box_center(scale, text, placement[k])
            s_svg += draw_line(x1=center_parent[0],
                               y1=center_parent[1],
                               x2=center_child[0],
                               y2=center_child[1],
                               scale=scale,
                               color='#000000',
                               opacity=0.8)

    x_min = sys.float_info.max
    y_min = sys.float_info.max
    x_max = -sys.float_info.max
    y_max = -sys.float_info.max

    # later we place the nodes so that they show up "on top"
    for node in commits:
        (_, _, name) = node
        (x, y) = placement[node]
        width, height = get_box_dims(scale, name)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x + width)
        y_max = max(y_max, y + height)
        stroke_color, fill_color = get_color(name)
        s_svg += draw_box(text=name,
                          x=x,
                          y=y,
                          scale=scale,
                          stroke_color=stroke_color,
                          fill_color=fill_color,
                          opacity=1.0,
                          rounded=True)

    # finally place branches and tags
    for node in pointers:
        (line_number, character_position, text, angle) = pointers[node][0]
        (x, y) = placement[(line_number, character_position, text)]
        (x_target, y_target) = get_box_center(scale, text, (x, y))
        (_, _, tag_text) = node
        target_width, target_height = get_box_dims(scale, text)

        # remove the starting [ and ending ]
        tag_text = tag_text[1:-1]

        # tags can be a comma separated list
        for tag in tag_text.split(','):
            tag_width, tag_height = get_box_dims(scale, tag)
            if angle == 0:
                x = x + 0.5 * target_width - 0.5 * tag_width
                y = y + target_height + scale * 35.0
            elif angle == 180:
                x = x + 0.5 * target_width - 0.5 * tag_width
                y = y - tag_height - scale * 35.0
            if angle == 90:
                x = x - tag_width - scale * 35.0
            elif angle == 270:
                x = x + target_width + scale * 35.0
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x + tag_width)
            y_max = max(y_max, y + tag_height)
            center_tag = get_box_center(scale, tag, (x, y))
            x2, y2 = arrow_head(arrow_origin_xy=center_tag,
                                box_center_xy=(x_target, y_target),
                                box_width=target_width,
                                box_height=target_height)
            # update target
            target_width, target_height = tag_width, tag_height
            (x_target, y_target) = center_tag
            if tag.startswith('_'):
                tag_opacity = 0.2
                fill_color = '#ffffff'
                _tag = tag[1:]
                ghost = True
            else:
                tag_opacity = 1.0
                fill_color = '#dddddd'
                _tag = tag
                ghost = False
            s_svg += draw_arrow(x1=center_tag[0],
                                y1=center_tag[1],
                                x2=x2,
                                y2=y2,
                                scale=scale,
                                color='#000000',
                                ghost=ghost)
            s_svg += draw_box(text=_tag,
                              x=x,
                              y=y,
                              scale=scale,
                              stroke_color='#000000',
                              fill_color=fill_color,
                              opacity=tag_opacity,
                              rounded=False)

    bbox = (x_min, y_min, x_max, y_max)
    s_svg = embed_svg(text=s_svg, bbox=(x_min, y_min, x_max, y_max))
    return s_svg
