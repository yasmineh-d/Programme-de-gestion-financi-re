import sqlite3


def create_database():
    conn = sqlite3.connect("financial_database.db")
    cursor = conn.cursor()

    # إنشاء جدول للمشتريات
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # إنشاء جدول للمبيعات
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    # إنشاء جدول للعملاء
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)

    # إنشاء جدول للحسابات
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            account_type TEXT NOT NULL,
            opening_balance REAL NOT NULL,
            creation_date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("تم إنشاء قاعدة البيانات والجداول بنجاح!")

def get_database_connection():
    """إنشاء اتصال بقاعدة البيانات"""
    conn = sqlite3.connect("financial_database.db")
    return conn

def insert_sample_data():
    conn = sqlite3.connect("financial_database.db")
    cursor = conn.cursor()

    # إضافة بيانات تجريبية إلى جدول الحسابات
    sample_accounts = [
        ("حساب التوفير", "توفير", 5000.0, "2025-01-01"),
        ("حساب جاري", "جاري", 15000.0, "2025-02-01"),
        ("حساب الاستثمار", "استثمار", 25000.0, "2025-03-01")
    ]

    cursor.executemany("INSERT INTO accounts (account_name, account_type, opening_balance, creation_date) VALUES (?, ?, ?, ?)", sample_accounts)

    conn.commit()
    conn.close()
    print("تمت إضافة البيانات التجريبية بنجاح!")

if __name__ == "__main__":
    create_database()
    insert_sample_data()