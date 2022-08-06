from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QFrame


class TitleBarWidget(QFrame):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        label = QLabel('Math Solver | by ZavaruKitsu')
        layout.addWidget(label, alignment=Qt.AlignLeft)

        layout.addSpacing(1000)

        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(QIcon('./assets/icons/minimize.svg'))
        self.minimize_btn.setFixedSize(24, 24)
        self.minimize_btn.clicked.connect(self.minimize_window)

        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon('./assets/icons/close.svg'))
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.clicked.connect(self.close_window)

        layout.addWidget(self.minimize_btn)
        layout.addSpacing(16)
        layout.addWidget(self.close_btn)

        self.setStyleSheet('''
        QFrame {
            border-width: 3px;
            border-style: solid;
            border-color: transparent transparent #f7f7f7 transparent;
        }
        
        QLabel {
            border: none;
        }
        
        QPushButton {
            background-color: transparent;
            border-radius: 12px;
        }
        
        QPushButton:hover {
            background-color: #f7f7f7;
        }
        ''')

        self.setLayout(layout)

    def minimize_window(self, *args):
        self.parent().showMinimized()

    def close_window(self, *args):
        self.parent().close()
