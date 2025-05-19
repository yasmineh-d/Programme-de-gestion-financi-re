from modules.database import get_database_connection

def create_database():
    conn = get_database_connection()
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

    conn.commit()
    conn.close()
    print("تم إنشاء قاعدة البيانات والجداول بنجاح!")

if __name__ == "__main__":
    create_database()