from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
with app.app_context():
    init_db()
app.secret_key = 'your_secret_key'  # Change this in production

DATABASE = 'expenses.db'
import os

if not os.path.exists(DATABASE):
    open(DATABASE, 'w').close()
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )''')
        db.commit()

@app.route('/')
def index():
    db = get_db()
    expenses = db.execute('SELECT * FROM expenses ORDER BY date DESC').fetchall()
    total_row = db.execute('SELECT SUM(amount) FROM expenses').fetchone()
    total = total_row[0] if total_row and total_row[0] is not None else 0
    category_rows = db.execute('SELECT category, SUM(amount) AS total_amount FROM expenses GROUP BY category').fetchall()
    categories = [{'category': row['category'], 'total_amount': row['total_amount']} for row in category_rows]
    db.close()
    return render_template('index.html', expenses=expenses, total=total, categories=categories)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']
        description = request.form['description']
        
        # Validation
        if not amount or not category or not date:
            flash('Amount, category, and date are required!')
            return redirect(url_for('add_expense'))
        try:
            amount = float(amount)
        except ValueError:
            flash('Amount must be a number!')
            return redirect(url_for('add_expense'))
        
        db = get_db()
        db.execute('INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)',
                   (amount, category, date, description))
        db.commit()
        db.close()
        flash('Expense added successfully!')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete_expense(id):
    db = get_db()
    db.execute('DELETE FROM expenses WHERE id = ?', (id,))
    db.commit()
    db.close()
    flash('Expense deleted successfully!')
    return redirect(url_for('index'))

@app.route('/filter', methods=['GET', 'POST'])
def filter_expenses():
    if request.method == 'POST':
        category = request.form.get('category')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        
        query = 'SELECT * FROM expenses WHERE 1=1'
        params = []
        if category:
            query += ' AND category = ?'
            params.append(category)
        if date_from:
            query += ' AND date >= ?'
            params.append(date_from)
        if date_to:
            query += ' AND date <= ?'
            params.append(date_to)
        query += ' ORDER BY date DESC'
        
        db = get_db()
        expenses = db.execute(query, params).fetchall()
        total = sum(row['amount'] for row in expenses)
        category_rows = db.execute('SELECT category, SUM(amount) AS total_amount FROM expenses GROUP BY category').fetchall()
        categories = [{'category': row['category'], 'total_amount': row['total_amount']} for row in category_rows]
        db.close()
        return render_template('index.html', expenses=expenses, total=total, categories=categories, filtered=True)
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
