import shutil
from collections.abc import Sequence
from zipfile import ZipFile

from loguru import logger

from tools import configs
from tools.configs import path_define
from tools.configs.options import FontFormat


def make_release_zips(font_formats: Sequence[FontFormat]) -> None:
    path_define.RELEASES_DIR.mkdir(parents=True, exist_ok=True)

    for font_format in font_formats:
        zip_file_path = path_define.RELEASES_DIR.joinpath(f'qrcode-pixel-font-{font_format}-v{configs.VERSION}.zip')
        with ZipFile(zip_file_path, 'w') as file:
            file.write(path_define.PROJECT_ROOT_DIR.joinpath('LICENSE-OFL'), 'OFL.txt')

            font_file_path = path_define.OUTPUTS_DIR.joinpath(f'qrcode-pixel.{font_format}')
            file.write(font_file_path, font_file_path.name)
        logger.info("Make release zip: '{}'", zip_file_path)


def update_www() -> None:
    if path_define.WWW_FONTS_DIR.exists():
        shutil.rmtree(path_define.WWW_FONTS_DIR)
    path_define.WWW_FONTS_DIR.mkdir(parents=True)

    for path_from in path_define.OUTPUTS_DIR.glob('*.otf.woff2'):
        if not path_from.is_file():
            continue

        path_to = path_from.copy_into(path_define.WWW_FONTS_DIR)
        logger.info("Copy file: '{}' -> '{}'", path_from, path_to)
