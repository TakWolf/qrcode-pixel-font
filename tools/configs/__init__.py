from typing import Literal, get_args

version = '1.3.0'
version_time = '2025-05-26'

type FontFormat = Literal['otf', 'otf.woff', 'otf.woff2', 'ttf', 'ttf.woff', 'ttf.woff2', 'bdf', 'pcf']
font_formats = list[FontFormat](get_args(FontFormat.__value__))
