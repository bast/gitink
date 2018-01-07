#!/usr/bin/env python

from distutils.core import setup

setup(name='gitink',
      version='0.1.0',
      description='Git Ink - an ASCII to SVG Git log graph visualizer.',
      author='Radovan Bast',
      author_email='bast@users.noreply.github.com',
      url='https://github.com/bast/gitink',
      packages=['gitink'],
      license='MPL-2.0',
      entry_points={
        'console_scripts': [
            'gitink = gitink.gitink:main'
            ]
        }
     )
