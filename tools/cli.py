import shutil

from cyclopts import App, Parameter
from loguru import logger

from tools import configs
from tools.configs import path_define, FontFormat
from tools.services import font_service, publish_service

app = App(
    version=configs.version,
    default_parameter=Parameter(consume_multiple=True),
)


@app.default
def main(
        cleanup: bool = False,
        font_formats: set[FontFormat] | None = None,
        release: bool = False,
):
    if font_formats is None:
        font_formats = configs.font_formats
    else:
        font_formats = sorted(font_formats, key=lambda x: configs.font_formats.index(x))

    logger.info('cleanup = {}', cleanup)
    logger.info('font_formats = {}', font_formats)
    logger.info('release = {}', release)

    if cleanup and path_define.build_dir.exists():
        shutil.rmtree(path_define.build_dir)
        logger.info("Delete dir: '{}'", path_define.build_dir)

    font_service.make_fonts(font_formats)

    if release:
        publish_service.make_release_zip(font_formats)

    if 'woff2' in font_formats:
        publish_service.update_www()


if __name__ == '__main__':
    app()