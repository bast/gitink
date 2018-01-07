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
  $ gitink example.txt | display

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


Contributions
-------------

Contributions are most welcome!

Suggestions:

-  Create a package and split into modules.
-  Disentangle.
-  Simplify.
-  Split long functions into smaller units.
-  Unit test functions.
-  Use named tuples instead of classes.
-  Avoid global variables.
