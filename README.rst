.. image:: https://travis-ci.org/bast/gitink.svg?branch=master
   :target: https://travis-ci.org/bast/gitink/builds
.. image:: https://img.shields.io/badge/license-%20MPL--v2.0-blue.svg
   :target: ../master/LICENSE


gitink
======

ASCII to SVG Git log graph visualizer. Useful for teaching Git.

.. code:: shell

  $ cat example.txt

                       [feature]
                        |
                 x1-----x2
                /
  c1----c2----m1----c3----c4
    \        /            |
     b1----b2----b3      [master,HEAD]
     |           |
    [_branch]   [branch]

  $ virtualenv venv
  $ source venv/bin/activate
  $ pip install git+https://github.com/bast/gitink@master

  $ gitink --help
  Usage: gitink [OPTIONS]

  Options:
    --scale FLOAT             Scale sizes by this factor.
    --in-file TEXT            ASCII file to convert.
    --time-direction INTEGER  Direction of the time arrow (0, 90, 180, or 270).
    --help                    Show this message and exit.

  $ gitink --time-direction=90 --in-file=example.txt | display

This produces (display command requires
`imagemagick <https://www.imagemagick.org>`__):

.. figure:: https://github.com/bast/gitink/raw/master/img/example.jpg
   :alt: Git log graph example


Installing
----------

As the software is not quite finished it isn’t in PyPI yet. You can
install it with pip by using

.. code:: shell

  $ pip install git+https://github.com/bast/gitink@master

Alternately you can replace master with a branch or a tag.


I used this code before but the API changed?
--------------------------------------------

You can find the old version on the ``spaghetti`` branch.
