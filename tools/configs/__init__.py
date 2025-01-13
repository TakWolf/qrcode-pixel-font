from typing import Literal, get_args

version = '1.1.0'
version_time = '2025-01-14'

type FontFormat = Literal['otf', 'ttf', 'woff2', 'bdf', 'pcf']
font_formats = list[FontFormat](get_args(FontFormat.__value__))
