class LexerException(Exception):
    def __init__(self, pos, *args):
        super(LexerException, self).__init__(*args)
        self.pos = pos


class EvaluatorException(Exception):
    pass
