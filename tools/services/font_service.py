import datetime
import unicodedata

import qrcode
from loguru import logger
from pixel_font_builder import FontBuilder, WeightName, SerifStyle, SlantStyle, WidthStyle, Glyph
from pixel_font_builder.opentype import Flavor
from pixel_font_knife.mono_bitmap import MonoBitmap
from qrcode.image.pure import PyPNGImage
from tqdm import tqdm

from tools import configs
from tools.configs import path_define, FontFormat


def make_fonts(font_formats: list[FontFormat]):
    builder = FontBuilder()
    builder.font_metric.font_size = 23
    builder.font_metric.horizontal_layout.ascent = 22
    builder.font_metric.horizontal_layout.descent = -1
    builder.font_metric.vertical_layout.ascent = 12
    builder.font_metric.vertical_layout.descent = -11
    builder.font_metric.x_height = 21
    builder.font_metric.cap_height = 21

    builder.meta_info.version = configs.version
    builder.meta_info.created_time = datetime.datetime.fromisoformat(f'{configs.version_time}T00:00:00Z')
    builder.meta_info.modified_time = builder.meta_info.created_time
    builder.meta_info.family_name = f'QRCode Pixel'
    builder.meta_info.weight_name = WeightName.REGULAR
    builder.meta_info.serif_style = SerifStyle.SANS_SERIF
    builder.meta_info.slant_style = SlantStyle.NORMAL
    builder.meta_info.width_style = WidthStyle.MONOSPACED
    builder.meta_info.manufacturer = 'TakWolf'
    builder.meta_info.designer = 'TakWolf'
    builder.meta_info.description = 'Displays characters as QR codes.'
    builder.meta_info.copyright_info = 'Copyright (c) 2025, TakWolf (https://takwolf.com).'
    builder.meta_info.license_info = 'This Font Software is licensed under the SIL Open Font License, Version 1.1.'
    builder.meta_info.vendor_url = 'https://qrcode-pixel-font.takwolf.com'
    builder.meta_info.designer_url = 'https://takwolf.com'
    builder.meta_info.license_url = 'https://openfontlicense.org'

    notdef_file_path = path_define.glyphs_dir.joinpath('notdef.png')
    notdef_bitmap = MonoBitmap.load_png(notdef_file_path)
    notdef_bitmap.save_png(notdef_file_path)
    builder.glyphs.append(Glyph(
        name='.notdef',
        horizontal_origin=(0, -1),
        advance_width=23,
        vertical_origin=(-11, 0),
        advance_height=23,
        bitmap=notdef_bitmap.data,
    ))

    alphabet = []
    for code_point in range(0x0000, 0xFFFF + 1):
        c = chr(code_point)
        if c.isprintable() or unicodedata.category(c) == 'Cc':
            alphabet.append(code_point)

    for code_point in tqdm(alphabet, desc='Make QRCodes'):
        image = qrcode.make(chr(code_point), image_factory=PyPNGImage)
        assert image.width == 21
        bitmap = MonoBitmap.create(21, 21)
        for y, qr_row in enumerate(image.modules):
            for x, flag in enumerate(qr_row):
                bitmap[y][x] = 1 if flag else 0
        bitmap = bitmap.resize(left=1, right=1, top=1, bottom=1)

        glyph_name = f'u{code_point:04X}'
        builder.character_mapping[code_point] = glyph_name
        builder.glyphs.append(Glyph(
            name=glyph_name,
            horizontal_origin=(0, -1),
            advance_width=23,
            vertical_origin=(-11, 0),
            advance_height=23,
            bitmap=bitmap.data,
        ))

    path_define.outputs_dir.mkdir(parents=True, exist_ok=True)

    for font_format in font_formats:
        file_path = path_define.outputs_dir.joinpath(f'qrcode-pixel.{font_format}')
        if font_format == 'woff2':
            builder.save_otf(file_path, flavor=Flavor.WOFF2)
        else:
            getattr(builder, f'save_{font_format}')(file_path)
        logger.info("Make font: '{}'", file_path)
