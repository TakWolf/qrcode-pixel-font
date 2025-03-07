from typing import Literal, get_args

version = '1.2.0'
version_time = '2025-02-25'

type FontFormat = Literal['otf', 'ttf', 'woff2', 'bdf', 'pcf']
font_formats = list[FontFormat](get_args(FontFormat.__value__))
