import sqlite3
import pandas as pd
from fpdf import FPDF

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

def export_to_excel():
    """تصدير البيانات من جدول الحسابات الختامية إلى ملف Excel"""
    try:
        connection = sqlite3.connect("financial_database.db")
        query = "SELECT * FROM final_accounts"
        df = pd.read_sql_query(query, connection)
        connection.close()

        # حفظ البيانات في ملف Excel
        df.to_excel("final_accounts.xlsx", index=False, engine='openpyxl')
        print("تم تصدير البيانات إلى ملف Excel بنجاح: final_accounts.xlsx")
    except Exception as e:
        print(f"حدث خطأ أثناء تصدير البيانات إلى Excel: {e}")

def export_to_pdf():
    """تصدير البيانات من جدول الحسابات الختامية إلى ملف PDF"""
    try:
        connection = sqlite3.connect("financial_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM final_accounts")
        rows = cursor.fetchall()
        connection.close()

        # إعداد ملف PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # إضافة عنوان
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 10, txt="تقرير الحسابات الختامية", ln=True, align="C")
        pdf.ln(10)

        # إضافة البيانات
        pdf.set_font("Arial", size=12)
        for row in rows:
            pdf.cell(0, 10, txt=str(row), ln=True)

        # حفظ ملف PDF
        pdf.output("final_accounts.pdf")
        print("تم تصدير البيانات إلى ملف PDF بنجاح: final_accounts.pdf")
    except Exception as e:
        print(f"حدث خطأ أثناء تصدير البيانات إلى PDF: {e}")

if __name__ == "__main__":
    # مثال على تعديل حساب ختامي
    update_final_accounts()
    edit_final_account(account_id=1, account_name="الإيرادات المعدلة", revenues=60000.0)
    # مثال على تصدير البيانات
    export_to_excel()
    export_to_pdf()
