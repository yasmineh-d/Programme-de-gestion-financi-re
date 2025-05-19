from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from main import get_database_connection  # استيراد الدالة إذا كانت موجودة في main.py

class PurchasesManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إضافة المشتريات")
        self.setGeometry(100, 100, 400, 400)
        layout = QVBoxLayout()

        # حقل إدخال اسم العنصر
        self.item_name_input = QLineEdit()
        self.item_name_input.setPlaceholderText("اسم العنصر")
        layout.addWidget(self.item_name_input)

        # حقل إدخال الكمية
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("الكمية")
        layout.addWidget(self.quantity_input)

        # حقل إدخال السعر
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("السعر")
        layout.addWidget(self.price_input)

        # حقل إدخال التاريخ
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("التاريخ (YYYY-MM-DD)")
        layout.addWidget(self.date_input)

        # زر الحفظ
        save_button = QPushButton("حفظ")
        save_button.clicked.connect(self.save_purchase)
        layout.addWidget(save_button)

        # زر الإغلاق
        close_button = QPushButton("إغلاق")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def save_purchase(self):
        """حفظ بيانات المشتريات في قاعدة البيانات"""
        item_name = self.item_name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()
        date = self.date_input.text()

        # التحقق من أن جميع الحقول ممتلئة
        if not item_name or not quantity or not price or not date:
            QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول!")
            return

        try:
            # الاتصال بقاعدة البيانات
            conn = get_database_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO purchases (item_name, quantity, price, date)
                VALUES (?, ?, ?, ?)
            """, (item_name, quantity, price, date))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "نجاح", "تم حفظ المشتريات بنجاح!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ: {e}")