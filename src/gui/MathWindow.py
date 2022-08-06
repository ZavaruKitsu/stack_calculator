import sys

from PySide6.QtGui import Qt, QPaintEvent, QPainter
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QVBoxLayout, QWidget, QApplication, QLabel

from .MathInput import MathInput
from .OptionsWidget import OptionsWidget, EvaluatorOptions
from .TitleBarWidget import TitleBarWidget
from .colors import *
from .. import EasyWrapper, solve_using_secant, integral_using_simpson

BORDER_RADIUS = 12


class MathWindow(QWidget):
    def __init__(self, app: QApplication):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedHeight(702)
        self.setFixedWidth(1050)

        self.app = app

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(24)
        shadow_effect.setOffset(0)
        shadow_effect.setColor(hex2QColor('EDEDED').darker())

        self.setGraphicsEffect(shadow_effect)

        layout = QVBoxLayout()
        layout.setContentsMargins(BORDER_RADIUS, BORDER_RADIUS, BORDER_RADIUS, BORDER_RADIUS)

        title_bar = TitleBarWidget()

        layout.addWidget(title_bar, 0, Qt.AlignTop)

        self.math_input = MathInput()
        self.math_input.expressionChanged.connect(self.expression_changed)

        layout.addWidget(self.math_input, 1, Qt.AlignHCenter | Qt.AlignTop)

        self.options_widget = OptionsWidget()
        self.options_widget.setVisible(False)
        self.options_widget.optionsChanged.connect(self.options_changed)

        self.options = EvaluatorOptions('Root', -10, 10, 0)

        layout.addWidget(self.options_widget, 3, Qt.AlignHCenter | Qt.AlignTop)

        self.result = QLabel()

        layout.addWidget(self.result, 1, Qt.AlignHCenter | Qt.AlignTop)

        self.setStyleSheet('''
        * {
            color: #424F6B;
        } 
        ''')

        self.setLayout(layout)

    def evaluate_expression(self, wrapper: EasyWrapper):
        res = wrapper(self.options.x)
        prefix = '⨍'

        if wrapper.lexer_result.is_function:
            prefix += '(x)'

        if res is not None:
            self.result.setText(f'{prefix} ≈ {res:.2f}')
        else:
            self.result.setText(f'{prefix} ∈ ∅')

    def solve_expression(self, wrapper: EasyWrapper):
        res = solve_using_secant(wrapper, self.options.a, self.options.b)

        if res is not None:
            evaluated = wrapper(res)
            self.result.setText(f'x ≈ {res:.2f}, ⨍({res:.2f}) ≈ {evaluated:.8f}')
        else:
            self.result.setText('x ∈ ∅')

    def integral_expression(self, wrapper: EasyWrapper):
        def f(i, N):
            self.result.setText(f'∫ step {i} / {N}')
            self.app.processEvents()

        res = integral_using_simpson(wrapper, self.options.a, self.options.b, f)

        if res is not None:
            self.result.setText(f'∫ ≈ {res:.2f}')
        else:
            self.result.setText('∫ ∈ ∅')

    def expression_changed(self):
        self.evaluate()

    def options_changed(self, options: EvaluatorOptions):
        self.options = options

        self.evaluate()

    def evaluate(self):
        if not self.math_input.valid:
            self.result.setText('')
            return

        wrapper = EasyWrapper(self.math_input.line_edit.text())

        self.options_widget.setVisible(wrapper.lexer_result.is_function)

        if not wrapper.lexer_result.is_function or self.options.mode == 'Expression':
            self.evaluate_expression(wrapper)
        elif self.options.mode == 'Root':
            self.solve_expression(wrapper)
        elif self.options.mode == 'Integral':
            self.integral_expression(wrapper)
        else:
            print('hto ya? dobavil noviy rezhim? ok, teper\' dobavlay handler v options_changed, debil...')
            sys.exit(-1)

    def paintEvent(self, event: QPaintEvent) -> None:
        # it's all about rounded corners...
        size = self.size()

        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing, True)

        qp.setPen(QColor(0, 0, 0, 0))
        qp.setBrush(QColor(0, 0, 0, 0))
        qp.drawRect(0, 0, size.width(), size.height())

        qp.setPen(BACKGROUND)
        qp.setBrush(BACKGROUND)
        qp.drawRoundedRect(BORDER_RADIUS, BORDER_RADIUS, size.width() - 2 * BORDER_RADIUS,
                           size.height() - 2 * BORDER_RADIUS, BORDER_RADIUS, BORDER_RADIUS)

        qp.end()
