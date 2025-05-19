from PyQt5 import QtWidgets, QtCore

def apply_rtl_styles(widget):
    """
    Apply RTL styles to the given widget.
    """
    widget.setLayoutDirection(QtCore.Qt.RightToLeft)
    widget.setStyleSheet("""
        QLabel {
            text-align: right;
        }
        QPushButton {
            text-align: right;
        }
        QLineEdit {
            text-align: right;
        }
        QTextEdit {
            text-align: right;
        }
        QListView {
            text-align: right;
        }
    """)

def set_rtl_font(widget, font_family='Arial', font_size=10):
    """
    Set the font for RTL support.
    """
    font = QtWidgets.QFont(font_family, font_size)
    widget.setFont(font)