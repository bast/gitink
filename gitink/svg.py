def get_box_dims(scale, text):
    width = scale * 8.0 * (len(text) + 2)
    height = scale * 30.0
    return width, height


def embed_svg(text, bbox):
    (x_min, y_min, x_max, y_max) = bbox
    height = y_max - y_min
    width = x_max - x_min

    return '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
              <!-- Created with GitInk -->
              <svg
                 xmlns:dc="http://purl.org/dc/elements/1.1/"
                 xmlns:cc="http://creativecommons.org/ns#"
                 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                 xmlns:svg="http://www.w3.org/2000/svg"
                 xmlns="http://www.w3.org/2000/svg"
                 xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
                 xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
                 width="{width}"
                 height="{height}"
                 id="svg2"
                 version="1.1"
                 inkscape:version="0.48.3.1 r9886"
                 sodipodi:docname="drawing.svg">

                <defs
                   id="defs4">
                  <marker
                     inkscape:stockid="fullmarker"
                     orient="auto"
                     refY="0.0"
                     refX="0.0"
                     id="fullmarker"
                     style="overflow:visible;">
                    <path
                       style="opacity:1.0;fill:#000000;stroke:#000000;fill-rule:evenodd;stroke-width:0.62500000;stroke-linejoin:round;"
                       d="M 8.7185878,4.0337352 L -2.2072895,0.016013256 L 8.7185884,-4.0017078 C 6.9730900,-1.6296469 6.9831476,1.6157441 8.7185878,4.0337352 z "
                       transform="scale(0.5) rotate(180) translate(0,0)" />
                  </marker>
                  <marker
                     inkscape:stockid="ghostmarker"
                     orient="auto"
                     refY="0.0"
                     refX="0.0"
                     id="ghostmarker"
                     style="overflow:visible;">
                    <path
                       style="opacity:0.2;fill:#000000;stroke:#000000;fill-rule:evenodd;stroke-width:0.62500000;stroke-linejoin:round;"
                       d="M 8.7185878,4.0337352 L -2.2072895,0.016013256 L 8.7185884,-4.0017078 C 6.9730900,-1.6296469 6.9831476,1.6157441 8.7185878,4.0337352 z "
                       transform="scale(0.5) rotate(180) translate(0,0)" />
                  </marker>
                </defs>
                <g inkscape:label="layer1"
                   inkscape:groupmode="layer"
                   transform="translate({translate_x},{translate_y}) rotate(0)"
                   id="layer1">
                   {text}
                </g>
              </svg>'''.format(width=width,
                               height=height,
                               translate_x=-x_min,
                               translate_y=-y_min,
                               text=text)


def draw_line(x1,
              y1,
              x2,
              y2,
              scale,
              color,
              opacity):

    return '''
           <line x1="{x1}"
                 y1="{y1}"
                 x2="{x2}"
                 y2="{y2}"
                 style="stroke:{color};
                        stroke-width:{width};
                        stroke-opacity:{opacity}" />
           '''.format(x1=x1,
                      y1=y1,
                      x2=x2,
                      y2=y2,
                      color=color,
                      width=scale * 2.5,
                      opacity=opacity)


def draw_arrow(x1,
               y1,
               x2,
               y2,
               scale,
               color,
               ghost):

    if ghost:
        opacity = 0.2
        marker = 'ghostmarker'
    else:
        opacity = 1.0
        marker = 'fullmarker'

    return '''
           <path style="fill:none;
                 stroke:{color};
                 stroke-width:{width};
                 stroke-linecap:butt;
                 stroke-linejoin:miter;
                 stroke-opacity:{opacity};
                 marker-end:url(#{marker});
                 stroke-miterlimit:4;
                 stroke-dasharray:none"
                 d="M {x1},{y1} {x2},{y2}"
                 inkscape:connector-curvature="0" />
           '''.format(x1=x1,
                      y1=y1,
                      x2=x2,
                      y2=y2,
                      color=color,
                      width=scale * 2.5,
                      opacity=opacity,
                      marker=marker)


def draw_box(text,
             x,
             y,
             scale,
             stroke_color,
             fill_color,
             opacity,
             rounded):

    width, height = get_box_dims(scale, text)
    text_x = x + scale * 7.5
    text_y = y + scale * 12.5 + 8.0
    if rounded:
        rounding = scale * 5.0
    else:
        rounding = 0.0
    font_size = scale * 12.5
    stroke_width = scale * 1.25

    return '''
           <rect style="fill:{fill_color};
                        stroke:{stroke_color};
                        stroke-width:{stroke_width};
                        stroke-miterlimit:4;
                        stroke-opacity:{opacity};
                        stroke-dasharray:none"
                 width="{width}"
                 height="{height}"
                 x="{x}"
                 y="{y}"
                 ry="{rounding}" />
           <text style="font-size:{font_size}px;
                        font-style:normal;
                        font-weight:normal;
                        line-height:125%%;
                        letter-spacing:0px;
                        word-spacing:0px;
                        fill:#000000;
                        fill-opacity:{opacity};
                        stroke:none;
                        font-family:DejaVu Sans Mono"
                 x="{text_x}"
                 y="{text_y}">{text}</text>
           '''.format(fill_color=fill_color,
                      stroke_color=stroke_color,
                      stroke_width=stroke_width,
                      width=width,
                      height=height,
                      x=x,
                      y=y,
                      text_x=text_x,
                      text_y=text_y,
                      rounding=rounding,
                      font_size=font_size,
                      opacity=opacity,
                      text=text)
