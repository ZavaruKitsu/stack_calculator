import math
import unittest

from src import Lexer, Tokenizer, Token, Converter, Evaluator, LexerException, EvaluatorException, EasyWrapper


class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()

    def test_basic_operations(self):
        exp = '1+2-3*4/58^6-(-x)^-97+(-1.1)'
        res = self.lexer.parse(exp)

        self.assertEqual(
            ['1', '+', '2', '-', '3', '*', '4', '/', '58', '^', '6', '-', '(', '-x', ')', '^', '-97', '+', '(', '-1.1',
             ')'], res.result)

    def test_functions(self):
        exp = 'sin(x-2^-5)+log(-log(sin(f(x*x^2-9^(-9-x+sin(8))))))'
        res = self.lexer.parse(exp)

        self.assertEqual(
            ['sin', '(', 'x', '-', '2', '^', '-5', ')', '+', 'log', '(', '-log', '(', 'sin', '(', 'f', '(', 'x', '*',
             'x', '^', '2', '-', '9', '^', '(', '-9', '-', 'x', '+', 'sin', '(', '8', ')', ')', ')', ')', ')', ')'],
            res.result)

    def test_decimal(self):
        exp = '23942830428482304.93949394+99999999991,22^1338.228'
        res = self.lexer.parse(exp)

        self.assertEqual(['23942830428482304.93949394', '+', '99999999991.22', '^', '1338.228'], res.result)

    def test_throws1(self):
        with self.assertRaises(LexerException) as context:
            exp = '1+3//4'
            _ = self.lexer.parse(exp)

        self.assertEqual(4, context.exception.pos)

    def test_throws2(self):
        with self.assertRaises(LexerException) as context:
            exp = '1+(-x))'
            _ = self.lexer.parse(exp)

        self.assertEqual(6, context.exception.pos)

    def test_throws3(self):
        with self.assertRaises(LexerException) as context:
            exp = '771.22^/2'
            _ = self.lexer.parse(exp)

        self.assertEqual(7, context.exception.pos)

    def test_throws4(self):
        with self.assertRaises(LexerException) as context:
            exp = '771(.22'
            _ = self.lexer.parse(exp)

        self.assertEqual(3, context.exception.pos)

    def test_throws5(self):
        with self.assertRaises(LexerException) as context:
            exp = '771.(22'
            _ = self.lexer.parse(exp)

        self.assertEqual(4, context.exception.pos)

    def test_throws6(self):
        with self.assertRaises(LexerException) as context:
            exp = '1+(771.22)('
            _ = self.lexer.parse(exp)

        self.assertEqual(10, context.exception.pos)

    def test_throws7(self):
        with self.assertRaises(LexerException) as context:
            exp = 'x('
            _ = self.lexer.parse(exp)

        self.assertEqual(1, context.exception.pos)

    def test_throws8(self):
        with self.assertRaises(LexerException) as context:
            exp = '1+sin)'
            _ = self.lexer.parse(exp)

        self.assertEqual(5, context.exception.pos)

    def test_throws9(self):
        with self.assertRaises(LexerException) as context:
            exp = '1.1.3+2'
            _ = self.lexer.parse(exp)

        self.assertEqual(3, context.exception.pos)

    def test_throws10(self):
        with self.assertRaises(LexerException) as context:
            exp = 'cotan'
            _ = self.lexer.parse(exp)

        self.assertEqual(6, context.exception.pos)

    def test_result(self):
        exp = '1+2/3^4'
        res = self.lexer.parse(exp)

        self.assertEqual(['1', '+', '2', '/', '3', '^', '4'], res.result)
        self.assertEqual('1 + 2 / 3^4', str(res))
        self.assertEqual('LexerResult(1; +; 2; /; 3; ^; 4)', repr(res))


class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.tokenizer = Tokenizer()

    def test_tokenizing(self):
        exp = '1+2-3/4*5^6+(-x)/7*sin(x)'
        res = self.lexer.parse(exp)
        res = self.tokenizer.tokenize(res)

        self.assertEqual([('1', Token.INTEGER), ('+', Token.OPERATOR), ('2', Token.INTEGER), ('-', Token.OPERATOR),
                          ('3', Token.INTEGER), ('/', Token.OPERATOR), ('4', Token.INTEGER), ('*', Token.OPERATOR),
                          ('5', Token.INTEGER), ('^', Token.OPERATOR), ('6', Token.INTEGER), ('+', Token.OPERATOR),
                          ('(', Token.BRACKET_OPEN), ('-x', Token.VARIABLE), (')', Token.BRACKET_CLOSE),
                          ('/', Token.OPERATOR), ('7', Token.INTEGER), ('*', Token.OPERATOR), ('sin', Token.FUNCTION),
                          ('(', Token.BRACKET_OPEN), ('x', Token.VARIABLE), (')', Token.BRACKET_CLOSE)], res.result)

    def test_result(self):
        exp = '1+2-3/4*5^6+(-x)/7*sin(x)'
        lexer_res = self.lexer.parse(exp)
        res = self.tokenizer.tokenize(lexer_res)

        self.assertEqual(
            'TokenizerResult(("1", INTEGER); ("+", OPERATOR); ("2", INTEGER); ("-", OPERATOR); ("3", INTEGER); ("/", OPERATOR); ("4", INTEGER); ("*", OPERATOR); ("5", INTEGER); ("^", OPERATOR); ("6", INTEGER); ("+", OPERATOR); ("(", BRACKET_OPEN); ("-x", VARIABLE); (")", BRACKET_CLOSE); ("/", OPERATOR); ("7", INTEGER); ("*", OPERATOR); ("sin", FUNCTION); ("(", BRACKET_OPEN); ("x", VARIABLE); (")", BRACKET_CLOSE))',
            repr(res))
        self.assertEqual(str(lexer_res), str(res))


class TestConverter(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.tokenizer = Tokenizer()
        self.converter = Converter()

    def test_basic(self):
        exp = '(1+4/2^9)/2-(9*2-(23^3-3))^6'
        res = self.lexer.parse(exp)
        res = self.tokenizer.tokenize(res)
        res = self.converter.convert(res)

        self.assertEqual(
            ['1', '4', '2', '9', '^', '/', '+', '2', '/', '9', '2', '*', '23', '3', '^', '3', '-', '-', '6', '^', '-'],
            [item[0] for item in res.result])

    def test_functions_and_variables(self):
        exp = '1+sin(x)^(log(2)+cos(x^2-1+cos(sqrt(x)^2)-1)^x)'
        res = self.lexer.parse(exp)
        res = self.tokenizer.tokenize(res)
        res = self.converter.convert(res)

        self.assertEqual(
            ['1', 'x', 'sin', '2', 'log', 'x', '2', '^', '1', '-', 'x', 'sqrt', '2', '^', 'cos', '+', '1', '-', 'cos',
             'x', '^', '+', '^', '+'], [item[0] for item in res.result])

    def test_result(self):
        exp = '(1+4/2^9)/2-(9*2-(23^3-3))^6'
        lexer_res = self.lexer.parse(exp)
        res = self.tokenizer.tokenize(lexer_res)
        res = self.converter.convert(res)

        self.assertEqual(
            'ConverterResult(("1", INTEGER); ("4", INTEGER); ("2", INTEGER); ("9", INTEGER); ("^", OPERATOR); ("/", OPERATOR); ("+", OPERATOR); ("2", INTEGER); ("/", OPERATOR); ("9", INTEGER); ("2", INTEGER); ("*", OPERATOR); ("23", INTEGER); ("3", INTEGER); ("^", OPERATOR); ("3", INTEGER); ("-", OPERATOR); ("-", OPERATOR); ("6", INTEGER); ("^", OPERATOR); ("-", OPERATOR))',
            repr(res))
        self.assertEqual(str(lexer_res), str(res))


class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.lexer = Lexer()
        self.tokenizer = Tokenizer()
        self.converter = Converter()
        self.evaluator = Evaluator()

    def get_result(self, exp: str, x: float = 0):
        res = self.lexer.parse(exp)
        res = self.tokenizer.tokenize(res)
        res = self.converter.convert(res)
        return self.evaluator.eval(res, x)

    def test_basic_operations(self):
        exp = f'1+5^2/9+sin({math.pi / 2})'
        res = self.get_result(exp)

        self.assertAlmostEqual(4.77777773, res)

    def test_x(self):
        exp = '1+x^2/7+log(-x-1)'
        res = self.get_result(exp, -8)

        self.assertAlmostEqual(12.088767291912456, res)

    def test_x2(self):
        exp = 'x-1'
        res = self.get_result(exp, 1)

        self.assertEqual(0, res)

    def test_divide_by_zero(self):
        exp = '1/0'
        res = self.get_result(exp)

        self.assertIsNone(res)

    def test_domain_error(self):
        exp = '1/log(-1)'
        res = self.get_result(exp)

        self.assertIsNone(res)

    def test_throws1(self):
        exp = '1/smth(-3)'

        with self.assertRaises(EvaluatorException):
            _ = self.get_result(exp)

    def test_throws2(self):
        exp = '1/2+3'
        res = self.lexer.parse(exp)
        res = self.tokenizer.tokenize(res)

        res.result.append(('[', Token.OPERATOR))
        res.result.append(('1', Token.INTEGER))

        res = self.converter.convert(res)

        with self.assertRaises(EvaluatorException):
            _ = self.evaluator.eval(res)


class TestWrapper(unittest.TestCase):
    def get_result(self, exp: str, x: float = 0):
        return EasyWrapper(exp)(x)

    def test_x(self):
        exp = 'x-1'
        res = self.get_result(exp, 1)

        self.assertEqual(0, res)
