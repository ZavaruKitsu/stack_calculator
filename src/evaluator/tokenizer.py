import logging
from enum import Enum
from typing import Tuple, List

from .consts import *
from .lexer import LexerResult

logger = logging.getLogger('Tokenizer')


class Token(Enum):
    INTEGER = 1
    VARIABLE = 2
    OPERATOR = 3
    FUNCTION = 4
    BRACKET_OPEN = 5
    BRACKET_CLOSE = 6


class TokenizerResult:
    def __init__(self, result: List[Tuple[str, Token]], lexer_result: LexerResult):
        self.result = result
        self.lexer_result = lexer_result

    def __str__(self):
        return str(self.lexer_result)

    def __repr__(self):
        s = '; '.join([f'("{item[0]}", {item[1].name})' for item in self.result])

        return f'TokenizerResult({s})'


class Tokenizer:
    def tokenize(self, lexer_result: LexerResult):
        assert lexer_result

        result: List[Tuple[str, Token]] = []

        for item in lexer_result.result:
            if item in OPERATORS:
                token = Token.OPERATOR
            elif item == SYMBOL_BRACKET_OPEN:
                token = Token.BRACKET_OPEN
            elif item == SYMBOL_BRACKET_CLOSE:
                token = Token.BRACKET_CLOSE
            else:
                abs_item = item.strip('-')

                if abs_item == SYMBOL_VARIABLE:
                    token = Token.VARIABLE
                elif all(ch in ALPHABET for ch in abs_item):
                    token = Token.FUNCTION
                else:
                    token = Token.INTEGER

            logger.debug(f'"{item}" is a(n) {token.name}')
            result.append((item, token))

        return TokenizerResult(result, lexer_result)
