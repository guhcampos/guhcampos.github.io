import sys
from pathlib import Path

from loguru import logger


def setup_logging(logdir: Path):
    logger.remove()

    fmt = "{time} - {name} - {level} - {message}"
    logger.add(logdir / "debug.log", level="DEBUG", format=fmt)
    logger.add(sys.stderr, level="INFO", format=fmt)
