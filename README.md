[![image](https://github.com/bast/gitink/workflows/Test/badge.svg)](https://github.com/bast/gitink/actions)
[![image](https://img.shields.io/badge/license-%20MPL--v2.0-blue.svg)](LICENSE)


# gitink

ASCII to SVG Git log graph visualizer. Useful for teaching Git.
Under the hood it uses https://github.com/bast/ascii2graph.


## Example

```console
$ cat example.txt

                     [feature]
                      |
                      v
               x1-----x2
              /
c1----c2----m1----c3----c4
  \        /            ^
   b1----b2----b3       |
   ^           ^       [master,HEAD]
   |           |
  [_branch]   [branch]
```

```bash
$ gitink --time-direction=90 --in-file=example.txt | display
```

This produces (display command requires
[imagemagick](https://www.imagemagick.org)):

![git log graph example](img/example.svg)


## Available options

```console
$ gitink --help

Usage: gitink [OPTIONS]

Options:
  --scale FLOAT             Scale sizes by this factor.
  --in-file TEXT            ASCII file to convert.
  --time-direction INTEGER  Direction of the time arrow (0, 90, 180, or 270).
  --help
```


## Installation

```bash
$ pip install gitink
```


## How do the colors work?

Coloring is done according to the first character of the commit hash.  Other
suggestions welcome.
