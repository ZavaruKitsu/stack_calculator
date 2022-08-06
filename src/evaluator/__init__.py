import logging
import sys

format = ' {name:10} {asctime}   {levelname:10} | {message}'
datefmt = '%I:%M:%S %p'
padding = ' ' * (format.index('|') + 1)


class ColoredFormatter(logging.Formatter):
    debug_color = '\033[36m'
    info_color = '\033[32m'
    warning_color = '\033[33m'
    error_color = '\033[31m'
    critical_color = '\033[31m' + '\033[1m'

    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: debug_color + format + reset,
        logging.INFO: info_color + format + reset,
        logging.WARNING: warning_color + format + reset,
        logging.ERROR: error_color + format + reset,
        logging.CRITICAL: critical_color + format + reset
    }
    FORMATTERS = {k: logging.Formatter(v, datefmt, '{') for k, v in FORMATS.items()}

    def format(self, record):
        formatter = self.FORMATTERS.get(record.levelno)
        return formatter.format(record)


colored_formatter = ColoredFormatter(style='{')


def create_console_handler():
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setLevel(logging.INFO)
    console_logger.setFormatter(colored_formatter)

    return console_logger


logging.basicConfig(format=format, datefmt=datefmt, style='{', level=logging.INFO, handlers=[create_console_handler()])

from .lexer import Lexer
from .tokenizer import Tokenizer, Token
from .converter import Converter
from .evaluator import Evaluator
from .solvers import *
from .consts import *
from .exceptions import *
