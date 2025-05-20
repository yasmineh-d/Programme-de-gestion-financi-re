from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QDialog, QMessageBox, QLineEdit, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
import sys
import sqlite3
import pandas as pd
from fpdf import FPDF
import os

# دالة لإنشاء اتصال بقاعدة البيانات
def get_database_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect("financial_database.db")
    return conn

def initialize_database():
    """إنشاء الجداول إذا لم تكن موجودة"""
    connection = get_database_connection()
    cursor = connection.cursor()
    
    # إنشاء جدول المشتريات إذا لم يكن موجودًا
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name TEXT NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    
    # إنشاء جدول المبيعات إذا لم يكن موجودًا
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    
    # إنشاء جدول الموردين إذا لم يكن موجودًا
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT
        )
    """)
    
    # إنشاء جدول العملاء إذا لم يكن موجودًا
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT
        )
    """)
    
    # إنشاء جدول المصاريف إذا لم يكن موجودًا
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_name TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    
    # إنشاء جدول الحسابات الختامية إذا لم يكن موجودًا
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS final_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            opening_balance REAL NOT NULL,
            revenues REAL NOT NULL,
            expenses REAL NOT NULL
        )
    """)

    # إنشاء جدول التقارير المالية إذا لم يكن موجودًا
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financial_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_name TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
    """)
    
    connection.commit()
    connection.close()

# نافذة إدارة المشتريات
class PurchasesManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة المشتريات")
        self.setGeometry(100, 100, 600, 400)

        # تحسين مظهر واجهة إدارة المشتريات
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 14px;
                color: #34495e;
                margin: 5px 0;
            }
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 8px;
                border: 2px solid #27ae60;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
            QTableWidget {
                background-color: #f9f9f9;
                border: 1px solid #dcdcdc;
                gridline-color: #e0e0e0;
                font-size: 12px;
                border-radius: 5px;
            }
            QLineEdit {
                border: 1px solid #bdc3c7;
                padding: 8px;
                font-size: 12px;
                border-radius: 5px;
                background-color: #ecf0f1;
            }
            QLineEdit:focus {
                border-color: #2ecc71;
            }
        """)

        layout = QVBoxLayout()

        # جدول عرض المشتريات
        self.table = QTableWidget()
        # تعديل الجدول ليشمل عمود ID
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "اسم المورد", "اسم المنتج", "الكمية", "السعر", "التاريخ"])
        layout.addWidget(self.table)

        # زر تحميل البيانات
        self.load_button = QPushButton("تحميل البيانات")
        self.load_button.clicked.connect(self.load_purchases)
        layout.addWidget(self.load_button)

        # حقول إدخال بيانات المشتريات
        self.supplier_name_label = QLabel("اسم المورد:")
        self.supplier_name_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.supplier_name_label)
        self.supplier_name_input = QLineEdit()
        self.supplier_name_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.supplier_name_input)

        self.product_name_label = QLabel("اسم المنتج:")
        self.product_name_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.product_name_label)
        self.product_name_input = QLineEdit()
        self.product_name_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.product_name_input)

        self.quantity_label = QLabel("الكمية:")
        self.quantity_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.quantity_label)
        self.quantity_input = QLineEdit()
        self.quantity_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.quantity_input)

        self.price_label = QLabel("السعر:")
        self.price_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.price_label)
        self.price_input = QLineEdit()
        self.price_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.price_input)

        self.date_label = QLabel("التاريخ:")
        self.date_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.date_label)
        self.date_input = QLineEdit()
        self.date_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.date_input)

        # زر الحفظ
        self.save_button = QPushButton("حفظ")
        self.save_button.setStyleSheet("text-align: right;")
        self.save_button.clicked.connect(self.save_purchase)
        layout.addWidget(self.save_button)

        # زر التعديل
        self.update_button = QPushButton("تعديل")
        self.update_button.setStyleSheet("text-align: right;")
        self.update_button.clicked.connect(self.update_purchase)
        layout.addWidget(self.update_button)

        # زر الحذف
        self.delete_button = QPushButton("حذف")
        self.delete_button.setStyleSheet("text-align: right;")
        self.delete_button.clicked.connect(self.delete_purchase)
        layout.addWidget(self.delete_button)

        # زر الإغلاق
        self.close_button = QPushButton("إغلاق")
        self.close_button.setStyleSheet("text-align: right;")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.table.itemSelectionChanged.connect(self.fill_fields_from_selection)

    def load_purchases(self):
        """تحميل بيانات المشتريات من قاعدة البيانات وعرضها في الجدول"""
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id, supplier_name, product_name, quantity, price, date FROM purchases")
            purchases = cursor.fetchall()
            connection.close()

            self.table.setRowCount(0)  # مسح البيانات القديمة
            for row_data in purchases:
                row_number = self.table.rowCount()
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل بيانات المشتريات: {e}")

    def save_purchase(self):
        """حفظ بيانات الشراء الجديد في قاعدة البيانات"""
        supplier_name = self.supplier_name_input.text()
        product_name = self.product_name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()
        date = self.date_input.text()

        if not all([supplier_name, product_name, quantity, price, date]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء الحقول المطلوبة")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO purchases (supplier_name, product_name, quantity, price, date) VALUES (?, ?, ?, ?, ?)",
                (supplier_name, product_name, quantity, price, date),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حفظ بيانات الشراء بنجاح")
            self.load_purchases()  # تحديث الجدول بعد الحفظ
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ: {e}")

    def update_purchase(self):
        """تعديل بيانات الشراء المحدد"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد الشراء الذي تريد تعديله")
            return

        purchase_id = self.table.item(selected_row, 0).text()  # جلب ID من العمود الأول
        supplier_name = self.supplier_name_input.text()
        product_name = self.product_name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()
        date = self.date_input.text()

        if not all([supplier_name, product_name, quantity, price, date]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء الحقول المطلوبة")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE purchases SET supplier_name = ?, product_name = ?, quantity = ?, price = ?, date = ? WHERE id = ?",
                (supplier_name, product_name, quantity, price, date, purchase_id),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم تعديل بيانات الشراء بنجاح")
            self.load_purchases()  # تحديث الجدول بعد التعديل
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التعديل: {e}")

    def delete_purchase(self):
        """حذف الشراء المحدد"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد الشراء الذي تريد حذفه")
            return

        purchase_id = self.table.item(selected_row, 0).text()  # جلب ID من العمود الأول

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM purchases WHERE id = ?", (purchase_id,))
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حذف الشراء بنجاح")
            self.load_purchases()  # تحديث الجدول بعد الحذف
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحذف: {e}")

    def fill_fields_from_selection(self):
        """ملء الحقول عند تحديد صف من الجدول"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return
        self.supplier_name_input.setText(self.table.item(selected_row, 1).text())
        self.product_name_input.setText(self.table.item(selected_row, 2).text())
        self.quantity_input.setText(self.table.item(selected_row, 3).text())
        self.price_input.setText(self.table.item(selected_row, 4).text())
        self.date_input.setText(self.table.item(selected_row, 5).text())

# نافذة إدارة المبيعات
class SalesManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة المبيعات")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        # جدول عرض المبيعات
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "اسم المنتج", "الكمية", "السعر", "التاريخ"])
        layout.addWidget(self.table)

        # زر تحميل البيانات
        self.load_button = QPushButton("تحميل البيانات")
        self.load_button.clicked.connect(self.load_sales)
        layout.addWidget(self.load_button)

        # حقول إدخال بيانات المبيعات
        self.product_name_label = QLabel("اسم المنتج:")
        self.product_name_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.product_name_label)
        self.product_name_input = QLineEdit()
        self.product_name_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.product_name_input)

        self.quantity_label = QLabel("الكمية:")
        self.quantity_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.quantity_label)
        self.quantity_input = QLineEdit()
        self.quantity_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.quantity_input)

        self.price_label = QLabel("السعر:")
        self.price_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.price_label)
        self.price_input = QLineEdit()
        self.price_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.price_input)

        self.date_label = QLabel("التاريخ:")
        self.date_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.date_label)
        self.date_input = QLineEdit()
        self.date_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.date_input)

        # زر الحفظ
        self.save_button = QPushButton("حفظ")
        self.save_button.setStyleSheet("text-align: right;")
        self.save_button.clicked.connect(self.save_sale)
        layout.addWidget(self.save_button)

        # زر التعديل
        self.update_button = QPushButton("تعديل")
        self.update_button.setStyleSheet("text-align: right;")
        self.update_button.clicked.connect(self.update_sale)
        layout.addWidget(self.update_button)

        # زر الحذف
        self.delete_button = QPushButton("حذف")
        self.delete_button.setStyleSheet("text-align: right;")
        self.delete_button.clicked.connect(self.delete_sale)
        layout.addWidget(self.delete_button)

        # زر الإغلاق
        self.close_button = QPushButton("إغلاق")
        self.close_button.setStyleSheet("text-align: right;")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.table.itemSelectionChanged.connect(self.fill_fields_from_selection)

    def load_sales(self):
        """تحميل بيانات المبيعات من قاعدة البيانات وعرضها في الجدول"""
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id, product_name, quantity, price, date FROM sales")
            sales = cursor.fetchall()
            connection.close()

            self.table.setRowCount(0)  # مسح البيانات القديمة
            for row_data in sales:
                row_number = self.table.rowCount()
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل بيانات المبيعات: {e}")

    def save_sale(self):
        """حفظ بيانات البيع الجديد في قاعدة البيانات"""
        product_name = self.product_name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()
        date = self.date_input.text()

        if not all([product_name, quantity, price, date]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء الحقول المطلوبة")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO sales (product_name, quantity, price, date) VALUES (?, ?, ?, ?)",
                (product_name, quantity, price, date),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حفظ بيانات البيع بنجاح")
            self.load_sales()  # تحديث الجدول بعد الحفظ
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ: {e}")

    def update_sale(self):
        """تعديل بيانات البيع المحدد"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد البيع الذي تريد تعديله")
            return

        sale_id = self.table.item(selected_row, 0).text()
        product_name = self.product_name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()
        date = self.date_input.text()

        if not all([product_name, quantity, price, date]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء الحقول المطلوبة")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE sales SET product_name = ?, quantity = ?, price = ?, date = ? WHERE id = ?",
                (product_name, quantity, price, date, sale_id),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم تعديل بيانات البيع بنجاح")
            self.load_sales()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التعديل: {e}")

    def delete_sale(self):
        """حذف البيع المحدد"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد البيع الذي تريد حذفه")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            sale_id = self.table.item(selected_row, 0).text()
            cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حذف البيع بنجاح")
            self.load_sales()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحذف: {e}")

    def fill_fields_from_selection(self):
        """ملء الحقول عند تحديد صف من الجدول"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return
        self.product_name_input.setText(self.table.item(selected_row, 1).text())
        self.quantity_input.setText(self.table.item(selected_row, 2).text())
        self.price_input.setText(self.table.item(selected_row, 3).text())
        self.date_input.setText(self.table.item(selected_row, 4).text())

# نافذة إدارة العملاء
class ClientsManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة العملاء")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        # جدول عرض العملاء
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "اسم العميل", "رقم الهاتف", "البريد الإلكتروني", "العنوان"])
        layout.addWidget(self.table)

        # زر تحميل البيانات
        self.load_button = QPushButton("تحميل البيانات")
        self.load_button.clicked.connect(self.load_clients)
        layout.addWidget(self.load_button)

        # حقول إدخال بيانات العملاء
        self.client_name_label = QLabel("اسم العميل:")
        self.client_name_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.client_name_label)
        self.client_name_input = QLineEdit()
        self.client_name_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.client_name_input)

        self.phone_label = QLabel("رقم الهاتف:")
        self.phone_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.phone_label)
        self.phone_input = QLineEdit()
        self.phone_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.phone_input)

        self.email_label = QLabel("البريد الإلكتروني:")
        self.email_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        self.email_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.email_input)

        self.address_label = QLabel("العنوان:")
        self.address_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.address_label)
        self.address_input = QLineEdit()
        self.address_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.address_input)

        # زر الحفظ
        self.save_button = QPushButton("حفظ")
        self.save_button.setStyleSheet("text-align: right;")
        self.save_button.clicked.connect(self.save_client)
        layout.addWidget(self.save_button)

        # زر التعديل
        self.update_button = QPushButton("تعديل")
        self.update_button.setStyleSheet("text-align: right;")
        self.update_button.clicked.connect(self.update_client)
        layout.addWidget(self.update_button)

        # زر الحذف
        self.delete_button = QPushButton("حذف")
        self.delete_button.setStyleSheet("text-align: right;")
        self.delete_button.clicked.connect(self.delete_client)
        layout.addWidget(self.delete_button)

        # زر الإغلاق
        self.close_button = QPushButton("إغلاق")
        self.close_button.setStyleSheet("text-align: right;")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.table.itemSelectionChanged.connect(self.fill_fields_from_selection)

    def load_clients(self):
        """تحميل بيانات العملاء من قاعدة البيانات وعرضها في الجدول"""
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id, client_name, phone, email, address FROM clients")
            clients = cursor.fetchall()
            connection.close()

            self.table.setRowCount(0)  # مسح البيانات القديمة
            for row_data in clients:
                row_number = self.table.rowCount()
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل بيانات العملاء: {e}")

    def save_client(self):
        """حفظ بيانات العميل الجديد في قاعدة البيانات"""
        client_name = self.client_name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()

        if not all([client_name, phone]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء الحقول المطلوبة")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO clients (client_name, phone, email, address) VALUES (?, ?, ?, ?)",
                (client_name, phone, email, address),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حفظ بيانات العميل بنجاح")
            self.load_clients()  # تحديث الجدول بعد الحفظ
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ: {e}")

    def update_client(self):
        """تعديل بيانات العميل المحدد"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد العميل الذي تريد تعديله")
            return

        client_id = self.table.item(selected_row, 0).text()
        client_name = self.client_name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()

        if not all([client_name, phone]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء الحقول المطلوبة")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE clients SET client_name = ?, phone = ?, email = ?, address = ? WHERE id = ?",
                (client_name, phone, email, address, client_id),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم تعديل بيانات العميل بنجاح")
            self.load_clients()  # تحديث الجدول بعد التعديل
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التعديل: {e}")

    def delete_client(self):
        """حذف العميل المحدد"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد العميل الذي تريد حذفه")
            return

        client_id = self.table.item(selected_row, 0).text()

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حذف العميل بنجاح")
            self.load_clients()  # تحديث الجدول بعد الحذف
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحذف: {e}")

    def fill_fields_from_selection(self):
        """ملء الحقول عند تحديد صف من الجدول"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return
        self.client_name_input.setText(self.table.item(selected_row, 1).text())
        self.phone_input.setText(self.table.item(selected_row, 2).text())
        self.email_input.setText(self.table.item(selected_row, 3).text())
        self.address_input.setText(self.table.item(selected_row, 4).text())

# نافذة إدارة الموردين
class SuppliersManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة الموردين")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        # جدول عرض الموردين
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "اسم المورد", "رقم الهاتف", "البريد الإلكتروني", "العنوان"])
        layout.addWidget(self.table)

        # زر تحميل البيانات
        self.load_button = QPushButton("تحميل البيانات")
        self.load_button.clicked.connect(self.load_suppliers)
        layout.addWidget(self.load_button)

        # حقول إدخال بيانات الموردين
        self.supplier_name_label = QLabel("اسم المورد:")
        self.supplier_name_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.supplier_name_label)
        self.supplier_name_input = QLineEdit()
        self.supplier_name_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.supplier_name_input)

        self.phone_label = QLabel("رقم الهاتف:")
        self.phone_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.phone_label)
        self.phone_input = QLineEdit()
        self.phone_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.phone_input)

        self.email_label = QLabel("البريد الإلكتروني:")
        self.email_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        self.email_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.email_input)

        self.address_label = QLabel("العنوان:")
        self.address_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.address_label)
        self.address_input = QLineEdit()
        self.address_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.address_input)

        # زر الحفظ
        self.save_button = QPushButton("حفظ")
        self.save_button.setStyleSheet("text-align: right;")
        self.save_button.clicked.connect(self.save_supplier)
        layout.addWidget(self.save_button)

        # زر التعديل
        self.update_button = QPushButton("تعديل")
        self.update_button.setStyleSheet("text-align: right;")
        self.update_button.clicked.connect(self.update_supplier)
        layout.addWidget(self.update_button)

        # زر الحذف
        self.delete_button = QPushButton("حذف")
        self.delete_button.setStyleSheet("text-align: right;")
        self.delete_button.clicked.connect(self.delete_supplier)
        layout.addWidget(self.delete_button)

        # زر الإغلاق
        self.close_button = QPushButton("إغلاق")
        self.close_button.setStyleSheet("text-align: right;")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.table.itemSelectionChanged.connect(self.fill_fields_from_selection)

    def load_suppliers(self):
        """تحميل بيانات الموردين من قاعدة البيانات وعرضها في الجدول"""
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id, supplier_name, phone, email, address FROM suppliers")
            suppliers = cursor.fetchall()
            connection.close()

            self.table.setRowCount(0)  # مسح البيانات القديمة
            for row_data in suppliers:
                row_number = self.table.rowCount()
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل بيانات الموردين: {e}")

    def save_supplier(self):
        """حفظ بيانات المورد الجديد في قاعدة البيانات"""
        supplier_name = self.supplier_name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()

        if not all([supplier_name, phone]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء الحقول المطلوبة")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO suppliers (supplier_name, phone, email, address) VALUES (?, ?, ?, ?)",
                (supplier_name, phone, email, address),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حفظ بيانات المورد بنجاح")
            self.load_suppliers()  # تحديث الجدول بعد الحفظ
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ: {e}")

    def update_supplier(self):
        """تعديل بيانات المورد المحدد"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد المورد الذي تريد تعديله")
            return

        supplier_id = self.table.item(selected_row, 0).text()
        supplier_name = self.supplier_name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        address = self.address_input.text()

        if not all([supplier_name, phone]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء الحقول المطلوبة")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE suppliers SET supplier_name = ?, phone = ?, email = ?, address = ? WHERE id = ?",
                (supplier_name, phone, email, address, supplier_id),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم تعديل بيانات المورد بنجاح")
            self.load_suppliers()  # تحديث الجدول بعد التعديل
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التعديل: {e}")

    def delete_supplier(self):
        """حذف المورد المحدد"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد المورد الذي تريد حذفه")
            return

        supplier_id = self.table.item(selected_row, 0).text()

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حذف المورد بنجاح")
            self.load_suppliers()  # تحديث الجدول بعد الحذف
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحذف: {e}")

    def fill_fields_from_selection(self):
        """ملء الحقول عند تحديد صف من الجدول"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return
        self.supplier_name_input.setText(self.table.item(selected_row, 1).text())
        self.phone_input.setText(self.table.item(selected_row, 2).text())
        self.email_input.setText(self.table.item(selected_row, 3).text())
        self.address_input.setText(self.table.item(selected_row, 4).text())

# نافذة إدارة المصاريف
class ExpensesManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة المصاريف")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        # جدول عرض المصاريف
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "اسم المصروف", "المبلغ", "التاريخ"])
        layout.addWidget(self.table)

        # زر تحميل البيانات
        self.load_button = QPushButton("تحميل البيانات")
        self.load_button.clicked.connect(self.load_expenses)
        layout.addWidget(self.load_button)

        # حقول إدخال بيانات المصاريف
        self.expense_name_label = QLabel("اسم المصروف:")
        self.expense_name_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.expense_name_label)
        self.expense_name_input = QLineEdit()
        self.expense_name_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.expense_name_input)

        self.amount_label = QLabel("المبلغ:")
        self.amount_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.amount_label)
        self.amount_input = QLineEdit()
        self.amount_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.amount_input)

        self.date_label = QLabel("التاريخ:")
        self.date_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.date_label)
        self.date_input = QLineEdit()
        self.date_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.date_input)

        # زر الحفظ
        self.save_button = QPushButton("حفظ")
        self.save_button.setStyleSheet("text-align: right;")
        self.save_button.clicked.connect(self.save_expense)
        layout.addWidget(self.save_button)

        # زر التعديل
        self.update_button = QPushButton("تعديل")
        self.update_button.setStyleSheet("text-align: right;")
        self.update_button.clicked.connect(self.update_expense)
        layout.addWidget(self.update_button)

        # زر الحذف
        self.delete_button = QPushButton("حذف")
        self.delete_button.setStyleSheet("text-align: right;")
        self.delete_button.clicked.connect(self.delete_expense)
        layout.addWidget(self.delete_button)

        # زر الإغلاق
        self.close_button = QPushButton("إغلاق")
        self.close_button.setStyleSheet("text-align: right;")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.table.itemSelectionChanged.connect(self.fill_fields_from_selection)

    def load_expenses(self):
        """تحميل بيانات المصاريف من قاعدة البيانات وعرضها في الجدول"""
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT id, expense_name, amount, date FROM expenses")
            expenses = cursor.fetchall()
            connection.close()

            self.table.setRowCount(0)  # مسح البيانات القديمة
            for row_data in expenses:
                row_number = self.table.rowCount()
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل بيانات المصاريف: {e}")

    def save_expense(self):
        """حفظ بيانات المصروف الجديد في قاعدة البيانات"""
        expense_name = self.expense_name_input.text()
        amount = self.amount_input.text()
        date = self.date_input.text()

        if not all([expense_name, amount, date]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء الحقول المطلوبة")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO expenses (expense_name, amount, date) VALUES (?, ?, ?)",
                (expense_name, amount, date),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حفظ بيانات المصروف بنجاح")
            self.load_expenses()  # تحديث الجدول بعد الحفظ
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحفظ: {e}")

    def update_expense(self):
        """تعديل بيانات المصروف المحدد"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد المصروف الذي تريد تعديله")
            return

        expense_id = self.table.item(selected_row, 0).text()
        expense_name = self.expense_name_input.text()
        amount = self.amount_input.text()
        date = self.date_input.text()

        if not all([expense_name, amount, date]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء الحقول المطلوبة")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE expenses SET expense_name = ?, amount = ?, date = ? WHERE id = ?",
                (expense_name, amount, date, expense_id),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم تعديل بيانات المصروف بنجاح")
            self.load_expenses()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء التعديل: {e}")

    def delete_expense(self):
        """حذف المصروف المحدد"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "خطأ", "يرجى تحديد المصروف الذي تريد حذفه")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            expense_id = self.table.item(selected_row, 0).text()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حذف المصروف بنجاح")
            self.load_expenses()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء الحذف: {e}")

    def fill_fields_from_selection(self):
        """ملء الحقول عند تحديد صف من الجدول"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            return
        self.expense_name_input.setText(self.table.item(selected_row, 1).text())
        self.amount_input.setText(self.table.item(selected_row, 2).text())
        self.date_input.setText(self.table.item(selected_row, 3).text())

# نافذة عرض الحسابات الختامية
class FinalAccountsManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("الحسابات الختامية")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        # جدول لعرض الحسابات الختامية
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["اسم الحساب", "الرصيد الافتتاحي", "الإيرادات", "المصروفات"])
        layout.addWidget(self.table_widget)

        # زر تحميل البيانات
        self.load_button = QPushButton("تحميل البيانات")
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button)

        # زر تصدير إلى Excel
        self.export_excel_button = QPushButton("تصدير إلى Excel")
        self.export_excel_button.clicked.connect(self.export_to_excel)
        layout.addWidget(self.export_excel_button)

        # زر الإغلاق
        self.close_button = QPushButton("إغلاق")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def load_data(self):
        """تحميل بيانات الحسابات الختامية من قاعدة البيانات وعرضها في الجدول"""
        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT account_name, opening_balance, revenues, expenses 
                FROM final_accounts
            """)
            rows = cursor.fetchall()
            connection.close()

            self.table_widget.setRowCount(0)  # مسح البيانات القديمة
            for row in rows:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                for column, value in enumerate(row):
                    self.table_widget.setItem(row_position, column, QTableWidgetItem(str(value)))

            QMessageBox.information(self, "نجاح", "تم تحميل البيانات بنجاح")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل البيانات: {e}")

    def export_to_excel(self):
        """تصدير البيانات إلى ملف Excel"""
        try:
            connection = get_database_connection()
            query = "SELECT * FROM final_accounts"
            df = pd.read_sql_query(query, connection)
            connection.close()

            # حفظ البيانات في ملف Excel
            df.to_excel("final_accounts.xlsx", index=False, engine='openpyxl')
            QMessageBox.information(self, "نجاح", "تم تصدير البيانات إلى ملف Excel بنجاح: final_accounts.xlsx")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تصدير البيانات إلى Excel: {e}")

# نافذة عرض التقارير المالية
class ReportsManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("التقارير المالية")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        # جدول لعرض التقارير المالية
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["نوع التقرير", "الوصف", "القيمة", "التاريخ"])
        layout.addWidget(self.table_widget)

        # زر تحميل التقارير
        self.load_button = QPushButton("تحميل التقارير")
        self.load_button.clicked.connect(self.load_reports)
        layout.addWidget(self.load_button)

        # زر تصدير إلى Excel
        self.export_excel_button = QPushButton("تصدير إلى Excel")
        self.export_excel_button.clicked.connect(self.export_to_excel)
        layout.addWidget(self.export_excel_button)

        # زر الإغلاق
        self.close_button = QPushButton("إغلاق")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def load_reports(self):
        """تحميل التقارير المالية بناءً على البيانات المدخلة"""
        try:
            connection = get_database_connection()
            cursor = connection.cursor()

            # استعلام لجلب إجمالي المبيعات
            cursor.execute("SELECT SUM(price * quantity) AS total_sales FROM sales")
            total_sales = cursor.fetchone()[0] or 0.0

            # استعلام لجلب إجمالي المصروفات
            cursor.execute("SELECT SUM(amount) AS total_expenses FROM expenses")
            total_expenses = cursor.fetchone()[0] or 0.0

            # استعلام لجلب إجمالي المشتريات
            cursor.execute("SELECT SUM(price * quantity) AS total_purchases FROM purchases")
            total_purchases = cursor.fetchone()[0] or 0.0

            # حساب الأرباح
            total_profit = total_sales - total_expenses

            # إعداد البيانات للتقرير
            self.reports = [
                ("إجمالي المبيعات", "إجمالي قيمة المبيعات", total_sales, ""),
                ("إجمالي المصروفات", "إجمالي قيمة المصروفات", total_expenses, ""),
                ("إجمالي المشتريات", "إجمالي قيمة المصروفات", total_purchases, ""),
                ("إجمالي الأرباح", "إجمالي الأرباح بعد المصروفات", total_profit, ""),
            ]

            # عرض البيانات في الجدول
            self.table_widget.setRowCount(0)
            for report in self.reports:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                for column, value in enumerate(report):
                    self.table_widget.setItem(row_position, column, QTableWidgetItem(str(value)))

            QMessageBox.information(self, "نجاح", "تم تحميل التقارير بنجاح")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل التقارير: {e}")
        finally:
            connection.close()

    def export_to_excel(self):
        """تصدير التقرير المالي إلى ملف Excel"""
        try:
            # تحويل البيانات إلى DataFrame
            df = pd.DataFrame(self.reports, columns=["نوع التقرير", "الوصف", "القيمة", "التاريخ"])

            # فتح مربع حوار لاختيار مسار الحفظ
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "حفظ التقرير المالي كملف Excel",
                os.path.join(os.path.expanduser("~"), "financial_report.xlsx"),
                "Excel Files (*.xlsx)",
                options=options
            )

            if not file_path:  # إذا لم يتم اختيار مسار
                QMessageBox.warning(self, "إلغاء", "تم إلغاء عملية الحفظ.")
                return

            # حفظ البيانات في ملف Excel
            df.to_excel(file_path, index=False, engine='openpyxl')
            QMessageBox.information(self, "نجاح", f"تم تصدير التقرير المالي إلى ملف Excel بنجاح: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تصدير التقرير إلى Excel: {e}")

# نافذة تصدير التقارير المالية
class ExportReportDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تصدير التقرير المالي")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # حقول إدخال بيانات التقرير
        self.report_name_label = QLabel("اسم التقرير:")
        self.report_name_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.report_name_label)
        self.report_name_input = QLineEdit()
        self.report_name_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.report_name_input)

        self.description_label = QLabel("الوصف:")
        self.description_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.description_label)
        self.description_input = QLineEdit()
        self.description_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.description_input)

        self.date_label = QLabel("التاريخ:")
        self.date_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.date_label)
        self.date_input = QLineEdit()
        self.date_input.setAlignment(Qt.AlignRight)
        layout.addWidget(self.date_input)

        # زر حفظ التقرير
        self.save_report_button = QPushButton("حفظ التقرير")
        self.save_report_button.setStyleSheet("text-align: right;")
        self.save_report_button.clicked.connect(self.save_report)
        layout.addWidget(self.save_report_button)

        # زر الإغلاق
        self.close_button = QPushButton("إغلاق")
        self.close_button.setStyleSheet("text-align: right;")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def save_report(self):
        """حفظ التقرير المالي إلى قاعدة البيانات"""
        report_name = self.report_name_input.text()
        description = self.description_input.text()
        date = self.date_input.text()

        if not all([report_name, description, date]):
            QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO financial_reports (report_name, description, date) VALUES (?, ?, ?)",
                (report_name, description, date),
            )
            connection.commit()
            connection.close()
            QMessageBox.information(self, "نجاح", "تم حفظ التقرير المالي بنجاح")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء حفظ التقرير المالي: {e}")

# النافذة الرئيسية
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("برنامج المحاسبة المالية")
        self.setGeometry(100, 100, 600, 400)

        # تحسين المظهر العام للنافذة الرئيسية
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f4f8;
            }
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 15px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
                margin: 5px 0;
                border: 2px solid #2980b9;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c5980;
            }
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #bdc3c7;
                gridline-color: #e0e0e0;
                font-size: 14px;
                border-radius: 5px;
            }
            QLineEdit {
                border: 1px solid #bdc3c7;
                padding: 8px;
                font-size: 14px;
                border-radius: 5px;
                background-color: #ecf0f1;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)

        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        title_label = QLabel("مرحبًا بكم في برنامج المحاسبة المالية")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # تحسين الأزرار في النافذة الرئيسية
        sections = [
            ("إدارة المشتريات", self.show_purchases_manager),
            ("إدارة المبيعات", self.show_sales_manager),
            ("إدارة العملاء", self.show_clients_manager),
            ("إدارة الموردين", self.show_suppliers_manager),
            ("إدارة المصاريف", self.show_expenses_manager),
            ("عرض الحسابات الختامية", self.show_final_accounts_manager),
            ("عرض التقارير المالية", self.show_reports_manager),
        ]

        for section_title, section_function in sections:
            button = QPushButton(section_title)
            button.clicked.connect(section_function)
            layout.addWidget(button)

    def show_purchases_manager(self):
        self.purchases_window = PurchasesManager()
        self.purchases_window.exec_()

    def show_sales_manager(self):
        self.sales_window = SalesManager()
        self.sales_window.exec_()

    def show_clients_manager(self):
        self.clients_window = ClientsManager()
        self.clients_window.exec_()

    def show_suppliers_manager(self):
        self.suppliers_window = SuppliersManager()
        self.suppliers_window.exec_()

    def show_expenses_manager(self):
        self.expenses_window = ExpensesManager()
        self.expenses_window.exec_()

    def show_final_accounts_manager(self):
        self.final_accounts_window = FinalAccountsManager()
        self.final_accounts_window.exec_()

    def show_reports_manager(self):
        self.reports_window = ReportsManager()
        self.reports_window.exec_()

class FinalAccountsReport(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تقرير الحسابات الختامية")
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        # جدول عرض تقرير الحسابات الختامية
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["اسم الحساب", "الرصيد الافتتاحي", "الإيرادات", "المصروفات"])
        layout.addWidget(self.table_widget)

        # زر تحميل التقرير
        self.load_button = QPushButton("تحميل التقرير")
        self.load_button.clicked.connect(self.update_and_load_report)  # ربط الزر بتحديث وتحميل التقرير
        layout.addWidget(self.load_button)

        # زر الإغلاق
        self.close_button = QPushButton("إغلاق")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def update_and_load_report(self):
        """تحديث الحسابات الختامية ثم تحميل التقرير"""
        try:
            update_final_accounts()  # تحديث الحسابات الختامية
            self.load_report()  # تحميل التقرير
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحديث أو تحميل التقرير: {e}")

    def load_report(self):
        """تحميل تقرير الحسابات الختامية من قاعدة البيانات"""
        try:
            connection = get_database_connection()
            cursor = connection.cursor()

            # استعلام لجلب البيانات من جدول الحسابات الختامية
            cursor.execute("""
                SELECT account_name, opening_balance, revenues, expenses 
                FROM final_accounts
            """)
            rows = cursor.fetchall()
            connection.close()

            self.table_widget.setRowCount(0)  # مسح البيانات القديمة
            for row in rows:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                for column, value in enumerate(row):
                    self.table_widget.setItem(row_position, column, QTableWidgetItem(str(value)))

            QMessageBox.information(self, "نجاح", "تم تحميل التقرير بنجاح")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"حدث خطأ أثناء تحميل التقرير: {e}")

def main():
    """الدالة الرئيسية لتشغيل البرنامج"""
    try:
        initialize_database()  # تأكد من إنشاء الجداول عند بدء التشغيل
        app = QApplication(sys.argv)
        window = MainWindow()  # إنشاء نافذة البرنامج الرئيسية
        window.show()  # عرض النافذة
        sys.exit(app.exec_())  # بدء الحلقة الرئيسية للتطبيق
    except Exception as e:
        print(f"حدث خطأ أثناء تشغيل البرنامج: {e}")

if __name__ == "__main__":
    main()  # استدعاء الدالة الرئيسية
