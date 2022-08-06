import logging
from typing import Tuple, List

from .consts import *
from .tokenizer import TokenizerResult, Token

logger = logging.getLogger('Converter')


class ConverterResult:
    def __init__(self, result: List[Tuple[str, Token]], tokenizer_result: TokenizerResult):
        self.result = result
        self.tokenizer_result = tokenizer_result

    def __str__(self):
        return str(self.tokenizer_result)

    def __repr__(self):
        s = '; '.join([f'("{item[0]}", {item[1].name})' for item in self.result])

        return f'ConverterResult({s})'


class Converter:
    def __init__(self):
        self._priority = {
            SYMBOL_BRACKET_OPEN: 1,
            SYMBOL_PLUS: 2,
            SYMBOL_MINUS: 2,
            SYMBOL_MULTIPLY: 3,
            SYMBOL_DIVIDE: 3,
            SYMBOL_DEGREE: 4,
            SYMBOL_BRACKET_CLOSE: 5
        }

    def _get_priority(self, item: Tuple[str, Token]):
        if item[1] == Token.FUNCTION:
            return 4

        return self._priority.get(item[0]) or 0

    def convert(self, tokenizer_result: TokenizerResult):
        assert tokenizer_result

        stack = []
        result = []

        for item in tokenizer_result.result:
            if item[1] in (Token.INTEGER, Token.VARIABLE):
                logger.debug(f'Pushing "{item}" to the result')
                result.append(item)
            elif item[1] == Token.FUNCTION:
                logger.debug(f'Pushing function "{item}" on the stack')
                stack.append(item)
            elif item[1] == Token.OPERATOR:
                priority = self._get_priority(item)
                logger.debug(
                    f'Got an operator "{item}" with priority "{priority}"')

                if stack and self._get_priority(stack[-1]) >= priority:
                    while stack and self._get_priority(stack[-1]) >= priority:
                        logger.debug(f'Pushing "{stack[-1]}" to the result from the stack')
                        result.append(stack.pop())

                logger.debug(f'Pushing "{item}" on the stack')
                stack.append(item)

            elif item[1] == Token.BRACKET_OPEN:
                logger.debug(f'Pushing "{item}" on the stack')
                stack.append(item)
            elif item[1] == Token.BRACKET_CLOSE:
                while stack[-1][1] != Token.BRACKET_OPEN:
                    logger.debug(f'Pushing "{stack[-1]}" on the stack')
                    result.append(stack.pop())

                logger.debug('Removing open bracket from the stack')
                stack.pop()  # remove open bracket
            else:
                logger.error('wtf')

        if stack:
            logger.debug('Pushing all contents from the stack to the result')
            while stack:
                result.append(stack.pop())

        return ConverterResult(result, tokenizer_result)
