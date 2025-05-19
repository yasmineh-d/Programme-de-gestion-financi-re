from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from modules.reports import ReportsManager  # استيراد ReportsManager
import tkinter as tk
from tkinter import ttk
from modules.database import get_database_connection

class SalesManager(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("إدارة المبيعات")
        self.geometry("400x300")
        self.configure(bg="white")

        # عناصر واجهة المستخدم
        tk.Label(self, text="اسم المنتج:", anchor="e", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.product_name_entry = tk.Entry(self)
        self.product_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="الكمية:", anchor="e", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="السعر:", anchor="e", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="التاريخ:", anchor="e", bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=3, column=1, padx=10, pady=5)

        self.save_button = tk.Button(self, text="حفظ", command=self.save_sale)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def save_sale(self):
        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        date = self.date_entry.get()

        if not all([product_name, quantity, price, date]):
            tk.messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO sales (product_name, quantity, price, date) VALUES (?, ?, ?, ?)",
                           (product_name, quantity, price, date))
            connection.commit()
            connection.close()
            tk.messagebox.showinfo("نجاح", "تم حفظ المبيعات بنجاح")
            self.destroy()
        except Exception as e:
            tk.messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ: {e}")

class ClientsManager(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("إدارة العملاء")
        self.geometry("400x300")
        self.configure(bg="white")

        # عناصر واجهة المستخدم
        tk.Label(self, text="اسم العميل:", anchor="e", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.client_name_entry = tk.Entry(self)
        self.client_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="رقم الهاتف:", anchor="e", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.phone_entry = tk.Entry(self)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="البريد الإلكتروني:", anchor="e", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = tk.Entry(self)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="العنوان:", anchor="e", bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.address_entry = tk.Entry(self)
        self.address_entry.grid(row=3, column=1, padx=10, pady=5)

        self.save_button = tk.Button(self, text="حفظ", command=self.save_client)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def save_client(self):
        client_name = self.client_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if not all([client_name, phone, email, address]):
            tk.messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO clients (client_name, phone, email, address) VALUES (?, ?, ?, ?)",
                           (client_name, phone, email, address))
            connection.commit()
            connection.close()
            tk.messagebox.showinfo("نجاح", "تم حفظ بيانات العميل بنجاح")
            self.destroy()
        except Exception as e:
            tk.messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ: {e}")

class AccountsManager(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("إدارة الحسابات")
        self.geometry("600x400")
        self.configure(bg="white")

        # عناصر واجهة المستخدم
        tk.Label(self, text="الحسابات", font=("Arial", 16), bg="white").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("#1", "#2", "#3", "#4"), show="headings")
        self.tree.heading("#1", text="اسم الحساب")
        self.tree.heading("#2", text="نوع الحساب")
        self.tree.heading("#3", text="الرصيد الافتتاحي")
        self.tree.heading("#4", text="تاريخ الإنشاء")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_button = tk.Button(self, text="تحميل الحسابات", command=self.load_accounts)
        self.load_button.pack(pady=5)

        self.add_button = tk.Button(self, text="إضافة حساب جديد", command=self.add_account)
        self.add_button.pack(pady=5)

    def load_accounts(self):
        try:
            connection = get_database_connection()
            cursor = connection.cursor()

            # استعلام للحصول على الحسابات
            cursor.execute("SELECT account_name, account_type, opening_balance, creation_date FROM accounts")
            accounts = cursor.fetchall()

            # مسح البيانات القديمة
            for row in self.tree.get_children():
                self.tree.delete(row)

            # إضافة البيانات إلى الجدول
            for account in accounts:
                self.tree.insert("", "end", values=account)

            connection.close()
        except Exception as e:
            tk.messagebox.showerror("خطأ", f"حدث خطأ أثناء تحميل الحسابات: {e}")

    def add_account(self):
        AddAccountWindow(self)

class AddAccountWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("إضافة حساب جديد")
        self.geometry("400x300")
        self.configure(bg="white")

        tk.Label(self, text="اسم الحساب:", anchor="e", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.account_name_entry = tk.Entry(self)
        self.account_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="نوع الحساب:", anchor="e", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.account_type_entry = tk.Entry(self)
        self.account_type_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="الرصيد الافتتاحي:", anchor="e", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.opening_balance_entry = tk.Entry(self)
        self.opening_balance_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="تاريخ الإنشاء:", anchor="e", bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.creation_date_entry = tk.Entry(self)
        self.creation_date_entry.grid(row=3, column=1, padx=10, pady=5)

        self.save_button = tk.Button(self, text="حفظ", command=self.save_account)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def save_account(self):
        account_name = self.account_name_entry.get()
        account_type = self.account_type_entry.get()
        opening_balance = self.opening_balance_entry.get()
        creation_date = self.creation_date_entry.get()

        if not all([account_name, account_type, opening_balance, creation_date]):
            tk.messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO accounts (account_name, account_type, opening_balance, creation_date) VALUES (?, ?, ?, ?)",
                           (account_name, account_type, opening_balance, creation_date))
            connection.commit()
            connection.close()
            tk.messagebox.showinfo("نجاح", "تم إضافة الحساب بنجاح")
            self.destroy()
        except Exception as e:
            tk.messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ: {e}")

class FinalAccountsManager(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("إدارة الحسابات الختامية")
        self.geometry("600x400")
        self.configure(bg="white")

        # عناصر واجهة المستخدم
        tk.Label(self, text="عرض الحسابات الختامية", font=("Arial", 16), bg="white").pack(pady=10)

        self.text_area = tk.Text(self, wrap="word", width=70, height=20)
        self.text_area.pack(padx=10, pady=10)

        self.load_button = tk.Button(self, text="تحميل البيانات", command=self.load_final_accounts)
        self.load_button.pack(pady=10)

    def load_final_accounts(self):
        try:
            connection = get_database_connection()
            cursor = connection.cursor()

            # استعلام للحصول على البيانات المالية (مثال: الأرباح والخسائر)
            cursor.execute("SELECT account_name, opening_balance FROM accounts")
            accounts = cursor.fetchall()

            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "الحسابات الختامية:\n\n")

            for account in accounts:
                self.text_area.insert(tk.END, f"اسم الحساب: {account[0]}, الرصيد الافتتاحي: {account[1]}\n")

            connection.close()
        except Exception as e:
            tk.messagebox.showerror("خطأ", f"حدث خطأ أثناء تحميل البيانات: {e}")

class PurchasesManager(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("إدارة المشتريات")
        self.geometry("400x300")
        self.configure(bg="white")

        # عناصر واجهة المستخدم
        tk.Label(self, text="اسم المورد:", anchor="e", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.supplier_name_entry = tk.Entry(self)
        self.supplier_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="اسم المنتج:", anchor="e", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.product_name_entry = tk.Entry(self)
        self.product_name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="الكمية:", anchor="e", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self, text="السعر:", anchor="e", bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self, text="التاريخ:", anchor="e", bg="white").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=4, column=1, padx=10, pady=5)

        self.save_button = tk.Button(self, text="حفظ", command=self.save_purchase)
        self.save_button.grid(row=5, column=0, columnspan=2, pady=10)

    def save_purchase(self):
        supplier_name = self.supplier_name_entry.get()
        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()
        date = self.date_entry.get()

        if not all([supplier_name, product_name, quantity, price, date]):
            tk.messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO purchases (supplier_name, product_name, quantity, price, date) VALUES (?, ?, ?, ?, ?)",
                           (supplier_name, product_name, quantity, price, date))
            connection.commit()
            connection.close()
            tk.messagebox.showinfo("نجاح", "تم حفظ بيانات المشتريات بنجاح")
            self.destroy()
        except Exception as e:
            tk.messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ: {e}")

class ExpensesManager(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("إدارة المصاريف")
        self.geometry("400x300")
        self.configure(bg="white")

        # عناصر واجهة المستخدم
        tk.Label(self, text="اسم المصروف:", anchor="e", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.expense_name_entry = tk.Entry(self)
        self.expense_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self, text="المبلغ:", anchor="e", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self, text="التاريخ:", anchor="e", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.date_entry = tk.Entry(self)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5)

        self.save_button = tk.Button(self, text="حفظ", command=self.save_expense)
        self.save_button.grid(row=3, column=0, columnspan=2, pady=10)

    def save_expense(self):
        expense_name = self.expense_name_entry.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()

        if not all([expense_name, amount, date]):
            tk.messagebox.showerror("خطأ", "يرجى ملء جميع الحقول")
            return

        try:
            connection = get_database_connection()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO expenses (expense_name, amount, date) VALUES (?, ?, ?)",
                           (expense_name, amount, date))
            connection.commit()
            connection.close()
            tk.messagebox.showinfo("نجاح", "تم حفظ المصروف بنجاح")
            self.destroy()
        except Exception as e:
            tk.messagebox.showerror("خطأ", f"حدث خطأ أثناء الحفظ: {e}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("برنامج المحاسبة المالية")
        self.layout = QVBoxLayout()  # إنشاء تخطيط رأسي
        self.container = QWidget()  # إنشاء حاوية
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)  # تعيين الحاوية كعنصر مركزي
        self.init_ui()  # استدعاء وظيفة إعداد واجهة المستخدم

    def init_ui(self):
        # إضافة عنوان رئيسي
        title_label = QLabel("مرحبًا بكم في برنامج المحاسبة المالية")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        # إضافة زر لإدارة الحسابات
        accounts_button = QPushButton("إدارة الحسابات")
        accounts_button.clicked.connect(self.show_accounts_manager)
        self.layout.addWidget(accounts_button)

        # إضافة زر لإدارة الفواتير
        transactions_button = QPushButton("إدارة الفواتير")
        transactions_button.clicked.connect(self.show_transactions_manager)
        self.layout.addWidget(transactions_button)

        # إضافة زر لتقارير الحسابات
        reports_button = QPushButton("عرض التقارير")
        reports_button.clicked.connect(self.show_reports_manager)
        self.layout.addWidget(reports_button)

        # إضافة زر لإدارة المبيعات
        sales_button = QPushButton("إدارة المبيعات")
        sales_button.clicked.connect(self.show_sales_manager)
        self.layout.addWidget(sales_button)

        # إضافة زر لإدارة العملاء
        clients_button = QPushButton("إدارة العملاء")
        clients_button.clicked.connect(self.show_clients_manager)
        self.layout.addWidget(clients_button)

        # إضافة زر لإدارة الحسابات الختامية
        final_accounts_button = QPushButton("إدارة الحسابات الختامية")
        final_accounts_button.clicked.connect(self.show_final_accounts_manager)
        self.layout.addWidget(final_accounts_button)

        # إضافة زر لإدارة المشتريات
        purchases_button = QPushButton("إدارة المشتريات")
        purchases_button.clicked.connect(self.show_purchases_manager)
        self.layout.addWidget(purchases_button)

        # إضافة زر لإدارة المصاريف
        expenses_button = QPushButton("إدارة المصاريف")
        expenses_button.clicked.connect(self.show_expenses_manager)
        self.layout.addWidget(expenses_button)

    def show_reports_manager(self):
        self.reports_window = ReportsManager()
        self.reports_window.exec_()

    def show_accounts_manager(self):
        self.accounts_window = AccountsManager()
        self.accounts_window.mainloop()

    def show_transactions_manager(self):
        QMessageBox.information(self, "إدارة الفواتير", "تم النقر على زر إدارة الفواتير")

    def show_sales_manager(self):
        self.sales_window = SalesManager()
        self.sales_window.mainloop()

    def show_clients_manager(self):
        self.clients_window = ClientsManager()
        self.clients_window.mainloop()

    def show_final_accounts_manager(self):
        self.final_accounts_window = FinalAccountsManager()
        self.final_accounts_window.mainloop()

    def show_purchases_manager(self):
        self.purchases_window = PurchasesManager()
        self.purchases_window.mainloop()

    def show_expenses_manager(self):
        self.expenses_window = ExpensesManager()
        self.expenses_window.mainloop()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())