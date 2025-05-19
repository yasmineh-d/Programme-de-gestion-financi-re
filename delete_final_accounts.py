import sqlite3

def update_final_accounts():
    """تحديث الحسابات الختامية بناءً على البيانات المسجلة في البرنامج"""
    try:
        connection = sqlite3.connect("financial_database.db")
        cursor = connection.cursor()

        # حذف جميع البيانات من جدول الحسابات الختامية
        cursor.execute("DELETE FROM final_accounts")
        connection.commit()

        # حساب إجمالي الإيرادات من جدول المبيعات
        cursor.execute("SELECT SUM(price * quantity) FROM sales")
        total_revenues = cursor.fetchone()[0] or 0.0

        # حساب إجمالي المصروفات من جدول المصروفات
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = cursor.fetchone()[0] or 0.0

        # حساب الأرباح (الإيرادات - المصروفات)
        total_profits = total_revenues - total_expenses

        # إدخال البيانات الجديدة إلى جدول الحسابات الختامية
        cursor.executemany("""
            INSERT INTO final_accounts (account_name, opening_balance, revenues, expenses)
            VALUES (?, ?, ?, ?)
        """, [
            ("الإيرادات", 0.0, total_revenues, 0.0),
            ("المصروفات", 0.0, 0.0, total_expenses),
            ("الأرباح", 0.0, total_profits, 0.0)
        ])

        connection.commit()
        connection.close()
        print("تم تحديث الحسابات الختامية بنجاح.")
    except Exception as e:
        print(f"حدث خطأ أثناء تحديث الحسابات الختامية: {e}")

def edit_final_account(account_id, account_name=None, opening_balance=None, revenues=None, expenses=None):
    """تعديل بيانات حساب ختامي معين"""
    try:
        connection = sqlite3.connect("financial_database.db")
        cursor = connection.cursor()

        # بناء استعلام التحديث ديناميكيًا بناءً على القيم المقدمة
        updates = []
        params = []
        if account_name is not None:
            updates.append("account_name = ?")
            params.append(account_name)
        if opening_balance is not None:
            updates.append("opening_balance = ?")
            params.append(opening_balance)
        if revenues is not None:
            updates.append("revenues = ?")
            params.append(revenues)
        if expenses is not None:
            updates.append("expenses = ?")
            params.append(expenses)

        if updates:
            query = f"UPDATE final_accounts SET {', '.join(updates)} WHERE id = ?"
            params.append(account_id)
            cursor.execute(query, params)
            connection.commit()
            print(f"تم تعديل الحساب الختامي بنجاح (ID: {account_id}).")
        else:
            print("لم يتم تقديم أي قيم لتعديل الحساب.")

        connection.close()
    except Exception as e:
        print(f"حدث خطأ أثناء تعديل الحساب الختامي: {e}")

if __name__ == "__main__":
    # مثال على تعديل حساب ختامي
    update_final_accounts()
    edit_final_account(account_id=1, account_name="الإيرادات المعدلة", revenues=60000.0)
