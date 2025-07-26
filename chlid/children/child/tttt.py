1from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(name)

# إنشاء قاعدة بيانات إذا ما موجودة
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            guardian TEXT,
            amount INTEGER,
            study_type TEXT,
            subscription_type TEXT
        )
    ''')
    conn.commit()
    conn.close()

# الصفحة الرئيسية (form)
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM children')
    children = c.fetchall()
    conn.close()
    return render_template('index.html', children=children)

# استقبال البيانات من الفورم
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    guardian = request.form['guardian']
    amount = request.form['amount']
    study_type = request.form['studyType']
    subscription_type = request.form['subscriptionType']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO children (name, guardian, amount, study_type, subscription_type) VALUES (?, ?, ?, ?, ?)',
              (name, guardian, amount, study_type, subscription_type))
    conn.commit()
    conn.close()
    return redirect('/')

if name == 'main':
    init_db()
    app.run(debug=True)