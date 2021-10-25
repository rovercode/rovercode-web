# -*- coding: utf-8 -*-
"""rovercode web app."""
__version__ = '0.1.0'
__version_info__ = tuple(  # pylint: disable=consider-using-generator
    [
        int(num) if num.isdigit() else num for num in __version__
        .replace('-', '.', 1).split('.')
    ]
)
