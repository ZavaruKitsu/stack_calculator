from .converter import Converter
from .evaluator import Evaluator, FUNCTIONS
from .exceptions import LexerException
from .lexer import Lexer
from .tokenizer import Tokenizer, Token


class EasyWrapper:
    def __init__(self, s):
        self.lexer = Lexer()
        self.tokenizer = Tokenizer()
        self.converter = Converter()
        self.evaluator = Evaluator()

        try:
            self.lexer_result = self.lexer.parse(s)
            self.valid = True
        except LexerException as err:
            self.lexer_result = None
            self.valid = False

            self.err = err

            return

        self.tokenizer_result = self.tokenizer.tokenize(self.lexer_result)
        for item in self.tokenizer_result.result:
            if item[1] == Token.FUNCTION:
                name = item[0].strip('-')
                if name not in FUNCTIONS:
                    self.valid = False
                    self.err = LexerException(-1, f'Unknown function "{name}"')

                    return

        self.converter_result = self.converter.convert(self.tokenizer_result)

    def __call__(self, x: float = 0):
        return self.evaluator.eval(self.converter_result, x)
