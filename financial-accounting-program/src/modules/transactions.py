from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class TransactionsManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة الفواتير")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # إضافة عنوان
        label = QLabel("هذه نافذة إدارة الفواتير")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # إضافة زر
        close_button = QPushButton("إغلاق")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)