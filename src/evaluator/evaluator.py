import logging
from typing import List, Tuple, Union

from .consts import *
from .converter import ConverterResult
from .exceptions import EvaluatorException
from .tokenizer import Token

logger = logging.getLogger('Evaluator')


class Evaluator:
    def __init__(self):
        self._operations = {
            SYMBOL_PLUS: lambda left, right: left + right,
            SYMBOL_MINUS: lambda left, right: left - right,
            SYMBOL_MULTIPLY: lambda left, right: left * right,
            SYMBOL_DIVIDE: lambda left, right: left / right,
            SYMBOL_DEGREE: lambda left, right: left ** right
        }

    def eval(self, converter_result: ConverterResult, x: float = 0):
        assert converter_result

        try:
            res = self._eval(converter_result.result, x)

            if not isinstance(res, float):
                res = float(res)

            return res
        except ZeroDivisionError:
            logger.debug('Unable to evaluate because of division by zero')
            return None
        except ValueError:
            logger.debug('Unable to evaluate because of domain error')
            return None

    def _eval(self, expression: List[Tuple[Union[str, int], Token]], x: float):
        stack = []

        for item in expression:
            if item[1] == Token.INTEGER:
                stack.append(item)
            elif item[1] == Token.VARIABLE:
                stack.append((self._eval_x(item, x), Token.INTEGER))
            elif item[1] == Token.OPERATOR:
                right = stack.pop()[0]
                left = stack.pop()[0]

                stack.append((self._eval_operator(item, left, right), Token.INTEGER))
            elif item[1] == Token.FUNCTION:
                value = stack.pop()[0]

                stack.append((self._eval_function(item, value), Token.INTEGER))
            else:
                logger.error('wtf')

        res = stack.pop()

        return res[0]

    def _eval_x(self, item: Tuple[Union[str, int], Token], x: float):
        assert item[1] == Token.VARIABLE

        if item[0].startswith('-'):
            return -x

        return x

    def _eval_operator(self, item: Tuple[Union[str, int], Token], left: str, right: str):
        assert item[1] == Token.OPERATOR

        func = self._operations.get(item[0])
        if not func:
            raise EvaluatorException(f'Unknown operation {item}')

        return func(float(left), float(right))

    def _eval_function(self, item: Tuple[str, Token], value: str):
        assert item[1] == Token.FUNCTION

        name = item[0]
        pos = True

        if name.startswith(SYMBOL_MINUS):
            name = item[0][1:]
            pos = False

        func = FUNCTIONS.get(name)
        if not func:
            raise EvaluatorException(f'Unknown function {name}')

        res = func(float(value))

        return res if pos else -res
