"""
gitink: ASCII to SVG Git log graph visualizer.
"""


from .version import version_info, __version__
from .main import main

__all__ = [
    "version_info",
    "main",
]
