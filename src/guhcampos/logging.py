import sys
from pathlib import Path

from loguru import logger


def setup_logging(logdir: Path):
    """
    This is a very basic loggins setup with loguru, focusing on providing a bit
    of extra safety in case I forget any debugs on.
    """
    logger.remove()

    fmt = "{time} - {name} - {level} - {message}"
    logger.add(sys.stderr, level="INFO", format=fmt)
    """
    Debug logs are only sent to file, as to avoid echoing potentially sensitive
    information to the Github Actions console.
    """
    logger.add(logdir / "debug.log", level="DEBUG", format=fmt)
