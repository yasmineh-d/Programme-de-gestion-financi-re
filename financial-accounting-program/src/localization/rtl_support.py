from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QPushButton, QDialog
from rtl_support import set_rtl_alignment

class ExampleDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مثال على دعم RTL")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        label = QLabel("هذا نص باللغة العربية")
        button = QPushButton("زر إغلاق")
        button.clicked.connect(self.close)

        layout.addWidget(label)
        layout.addWidget(button)
        self.setLayout(layout)

        # تطبيق دعم RTL
        set_rtl_alignment(self)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = ExampleDialog()
    dialog.exec_()