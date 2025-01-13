import shutil
import zipfile

from loguru import logger

from tools import configs
from tools.configs import path_define, FontFormat


def make_release_zip(font_formats: list[FontFormat]):
    path_define.releases_dir.mkdir(parents=True, exist_ok=True)
    for font_format in font_formats:
        file_path = path_define.releases_dir.joinpath(f'qrcode-pixel-font-{font_format}-v{configs.version}.zip')
        with zipfile.ZipFile(file_path, 'w') as file:
            file.write(path_define.project_root_dir.joinpath('LICENSE-OFL'), 'OFL.txt')
            font_file_name = f'qrcode-pixel.{font_format}'
            file.write(path_define.outputs_dir.joinpath(font_file_name), font_file_name)
        logger.info("Make release zip: '{}'", file_path)


def update_www():
    if path_define.www_fonts_dir.exists():
        shutil.rmtree(path_define.www_fonts_dir)
    path_define.www_fonts_dir.mkdir(parents=True)

    shutil.copyfile(path_define.outputs_dir.joinpath('qrcode-pixel.woff2'), path_define.www_fonts_dir.joinpath('qrcode-pixel.woff2'))
