from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QDialog
from PyQt5.QtCore import Qt

class AccountsManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة الحسابات")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # إضافة عنوان
        label = QLabel("هذه نافذة إدارة الحسابات")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # إضافة زر
        close_button = QPushButton("إغلاق")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

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

class ReportsManager(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("عرض التقارير")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # إضافة عنوان
        label = QLabel("هذه نافذة عرض التقارير")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # إضافة زر
        close_button = QPushButton("إغلاق")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("برنامج المحاسبة المالية")
        self.layout = QVBoxLayout()
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        self.init_ui()

    def init_ui(self):
        title_label = QLabel("مرحبًا بكم في برنامج المحاسبة المالية")
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        accounts_button = QPushButton("إدارة الحسابات")
        accounts_button.clicked.connect(self.show_accounts_manager)
        self.layout.addWidget(accounts_button)

        transactions_button = QPushButton("إدارة الفواتير")
        transactions_button.clicked.connect(self.show_transactions_manager)
        self.layout.addWidget(transactions_button)

        reports_button = QPushButton("عرض التقارير")
        reports_button.clicked.connect(self.show_reports_manager)
        self.layout.addWidget(reports_button)

    def show_accounts_manager(self):
        self.accounts_window = AccountsManager()
        self.accounts_window.exec_()

    def show_transactions_manager(self):
        self.transactions_window = TransactionsManager()
        self.transactions_window.exec_()

    def show_reports_manager(self):
        self.reports_window = ReportsManager()
        self.reports_window.exec_()

        purchases_button = QPushButton("إضافة المشتريات")
        purchases_button.clicked.connect(self.show_purchases_manager)
        self.layout.addWidget(purchases_button)
