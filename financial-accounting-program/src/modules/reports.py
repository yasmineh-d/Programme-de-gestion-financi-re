from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from modules.reports import ReportsManager

class ReportsManager(QDialog):
    def __init__(self):
        super().__init__()
        print("تم فتح نافذة عرض التقارير")  # تعليمات طباعة للتأكد
        self.setWindowTitle("عرض التقارير")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # إضافة عنوان
        label = QLabel("هذه نافذة عرض التقارير")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        print("تم إضافة العنوان")  # تعليمات طباعة للتأكد

        # إضافة زر
        close_button = QPushButton("إغلاق")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        print("تم إضافة زر الإغلاق")  # تعليمات طباعة للتأكد

        self.setLayout(layout)
        print("تم تعيين التخطيط")  # تعليمات طباعة للتأكد