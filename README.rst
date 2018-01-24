.. image:: https://travis-ci.org/bast/gitink.svg?branch=master
   :target: https://travis-ci.org/bast/gitink/builds
.. image:: https://img.shields.io/badge/license-%20MPL--v2.0-blue.svg
   :target: ../master/LICENSE


gitink
======

ASCII to SVG Git log graph visualizer. Useful for teaching Git.
Under the hood it uses https://github.com/bast/ascii2graph.


Example
-------

.. code:: shell

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

  $ gitink --time-direction=90 --in-file=example.txt | display

This produces (display command requires
`imagemagick <https://www.imagemagick.org>`__):

.. figure:: https://github.com/bast/gitink/raw/master/img/example.jpg
   :alt: Git log graph example


Available options
-----------------

.. code:: shell

  $ gitink --help
  Usage: gitink [OPTIONS]

  Options:
    --scale FLOAT             Scale sizes by this factor.
    --in-file TEXT            ASCII file to convert.
    --time-direction INTEGER  Direction of the time arrow (0, 90, 180, or 270).
    --help                    Show this message and exit.


Installation
------------

.. code:: shell

  $ pip install gitink

Alternately you can replace master with a branch or a tag.


How do the colors work?
-----------------------

Coloring is done according to the first character of the commit hash.  Other
suggestions welcome.


I used this code before but the API changed?
--------------------------------------------

You can find the old version on the ``spaghetti`` branch.
