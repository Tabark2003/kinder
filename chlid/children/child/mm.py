from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(name)

# الصفحة الرئيسية (تسجيل الأطفال)
@app.route('/')
def index():
    return render_template('index.html')

# صفحة الصادرات والواردات
@app.route('/finance', methods=['GET', 'POST'])
def finance():
    if request.method == 'POST':
        graduation_type = request.form['graduation']
        religion_event = float(request.form['religion'])
        maintenance = float(request.form['maintenance'])
        salaries = float(request.form['salaries'])
        others = float(request.form['others'])

        graduation_fee = 0
        if graduation_type == 'مدفوعة':
            graduation_fee = 100  # ممكن تغيير القيمة لاحقاً

        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute('''INSERT INTO finance_data (graduation_fee, religion_event, maintenance, salaries, others, date)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (graduation_fee, religion_event, maintenance, salaries, others, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
        return redirect(url_for('finance'))

    # عرض النتائج
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM finance_data')
    data = c.fetchall()
    conn.close()

    total_income = sum(row[1] for row in data)  # graduation_fee
    total_outcome = sum(row[2] + row[3] + row[4] + row[5] for row in data)
    profit = total_income - total_outcome

    return render_template('finance.html', data=data, income=total_income, outcome=total_outcome, profit=profit)


if name == 'main':
    # إنشاء قاعدة البيانات إذا ما موجودة
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS finance_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    graduation_fee REAL,
                    religion_event REAL,
                    maintenance REAL,
                    salaries REAL,
                    others REAL,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

    app.run(debug=True)