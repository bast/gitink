from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] < 3:
    with open(os.path.join(_here, 'README.rst')) as f:
        long_description = f.read()
else:
    with open(os.path.join(_here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()

version = {}
with open(os.path.join(_here, 'gitink', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='gitink',
    version=version['__version__'],
    description=('ASCII to SVG Git log graph visualizer.'),
    long_description=long_description,
    author='Radovan Bast',
    author_email='radovan.bast@uit.no',
    url='https://github.com/bast/gitink',
    license='MPL-2.0',
    packages=['gitink'],
    entry_points={
      'console_scripts': [
          'gitink = gitink.cli:cli'
          ]
      },
    install_requires=[
        'click==6.7.0',
        'ascii2graph==0.3.1',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6'],
    )
