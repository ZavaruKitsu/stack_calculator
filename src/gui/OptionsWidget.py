from dataclasses import dataclass

from PySide6.QtCore import Signal
from PySide6.QtGui import QDoubleValidator, Qt, QPainter
from PySide6.QtWidgets import QFrame, QVBoxLayout, QComboBox, QLineEdit, QLabel, QStyle, QStyleOptionComboBox


@dataclass(frozen=True)
class EvaluatorOptions:
    mode: str

    a: float
    b: float

    x: float


class QComboBoxWithoutArrow(QComboBox):
    def __init__(self):
        super().__init__()

        self.setFrame(False)

    def paintEvent(self, ev):
        qp = QPainter(self)

        opt = QStyleOptionComboBox()
        opt.initFrom(self)

        self.style().drawPrimitive(QStyle.PE_PanelButtonBevel, opt, qp, self)
        self.style().drawPrimitive(QStyle.PE_PanelButtonCommand, opt, qp, self)
        self.style().drawItemText(qp, self.rect(), Qt.AlignCenter, self.palette(), self.isEnabled(), self.currentText())

        qp.end()


class OptionsWidget(QFrame):
    optionsChanged = Signal(EvaluatorOptions)

    def __init__(self):
        super().__init__()

        self.setFixedWidth(300)

        self.doubleValidator = QDoubleValidator()

        layout = QVBoxLayout()

        layout.addWidget(QLabel('Evaluate'), 0, Qt.AlignHCenter)

        self.mode = QComboBoxWithoutArrow()
        self.mode.setFixedHeight(36)
        self.mode.addItems(['Root', 'Integral', 'Expression'])
        self.mode.currentTextChanged.connect(self.mode_changed)

        layout.addWidget(self.mode)

        layout.addSpacing(12)

        self.mode_label = QLabel('Intervals')

        layout.addWidget(self.mode_label, 0, Qt.AlignHCenter)

        self.interval_a = QLineEdit()
        self.interval_a.setFixedHeight(36)
        self.interval_a.setAlignment(Qt.AlignCenter)
        self.interval_a.setPlaceholderText('Start (a)')
        self.interval_a.setValidator(self.doubleValidator)
        self.interval_a.setText('-10')
        self.interval_a.textChanged.connect(self.smth_changed)

        layout.addWidget(self.interval_a)

        self.interval_b = QLineEdit()
        self.interval_b.setFixedHeight(36)
        self.interval_b.setAlignment(Qt.AlignCenter)
        self.interval_b.setPlaceholderText('End (b)')
        self.interval_b.setValidator(self.doubleValidator)
        self.interval_b.setText('10')
        self.interval_b.textChanged.connect(self.smth_changed)

        layout.addWidget(self.interval_b)

        self.variable = QLineEdit()
        self.variable.setFixedHeight(36)
        self.variable.setAlignment(Qt.AlignCenter)
        self.variable.setPlaceholderText('X')
        self.variable.setValidator(self.doubleValidator)
        self.variable.setText('0')
        self.variable.setVisible(False)
        self.variable.textChanged.connect(self.smth_changed)

        layout.addWidget(self.variable)

        self.setStyleSheet('''
        QFrame {
            border-width: 3px;
            border-style: solid;
            border-color: #f7f7f7;
            border-radius: 12px;
        }
        
        QLabel {
            border: none;
        }
        
        QLineEdit {
            border-radius: 18px;
        }
        
        QComboBoxWithoutArrow {
            border-width: 0px;
            
            background: white;
            padding: 4px 4px 4px 4px;
        }
        
        QComboBoxWithoutArrow QAbstractItemView {
            border-radius: 18px;
            
            background: white;
            padding: 4px 4px 4px 4px;
            
            selection-background-color: blue;
        }
        
        QComboBoxWithoutArrow QFrame {
            border-width: 0px;
            padding: 16px;
            background-color: transparent;
        }
        ''')

        self.setLayout(layout)

    def mode_changed(self, mode: str):
        is_x = mode == 'Expression'

        self.mode_label.setVisible(not is_x)
        self.interval_a.setVisible(not is_x)
        self.interval_b.setVisible(not is_x)
        self.variable.setVisible(is_x)

        self.emit_options()

    def smth_changed(self, *args, **kwrags):
        self.emit_options()

    def emit_options(self):
        a = float(self.interval_a.text() or '0')
        b = float(self.interval_b.text() or '0')
        x = float(self.variable.text() or '0')

        options = EvaluatorOptions(self.mode.currentText(), a, b, x)
        self.optionsChanged.emit(options)
