import math
import string

from inspect import isbuiltin, getmembers

#
# Operators
#

SYMBOL_PLUS = '+'
SYMBOL_MINUS = '-'
SYMBOL_MULTIPLY = '*'
SYMBOL_DIVIDE = '/'
SYMBOL_DEGREE = '^'

SYMBOL_BRACKET_OPEN = '('
SYMBOL_BRACKET_CLOSE = ')'

#
# etc.
#

SYMBOL_COMMA1 = '.'
SYMBOL_COMMA2 = ','

SYMBOL_VARIABLE = 'x'

#
# Combinations
#

OPERATORS = [SYMBOL_PLUS, SYMBOL_MINUS, SYMBOL_MULTIPLY, SYMBOL_DIVIDE, SYMBOL_DEGREE]
BRACKETS = [SYMBOL_BRACKET_OPEN, SYMBOL_BRACKET_CLOSE]
COMMAS = [SYMBOL_COMMA1, SYMBOL_COMMA2]
ALPHABET = string.ascii_letters + '_'

#
# Various
#

FUNCTIONS = {item[0]: item[1] for item in getmembers(math, isbuiltin)}
# giga-brain move
FUNCTIONS.update({f'co{item[0]}': lambda x, f=FUNCTIONS[item[0]]: 1.0 / f(x) for item in FUNCTIONS.items()})
FUNCTIONS['ln'] = math.log
FUNCTIONS['lb'] = math.log2
FUNCTIONS['lg'] = math.log10
FUNCTIONS['log_two'] = math.log2
FUNCTIONS['log_ten'] = math.log10
