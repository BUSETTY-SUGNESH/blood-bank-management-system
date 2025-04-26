
from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = os.path.join('instance', 'bloodbank.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash('Signup successful!', 'success')
        except:
            flash('Username already exists.', 'danger')
        conn.close()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/register_donor', methods=['GET', 'POST'])
def register_donor():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        blood_group = request.form['blood_group']
        conn = get_db_connection()
        conn.execute('INSERT INTO donor (DonorName, DonorAge, DonorGender, DonorBloodGroup) VALUES (?, ?, ?, ?)', (name, age, gender, blood_group))
        conn.commit()
        conn.close()
        flash('Donor Registered Successfully.', 'success')
        return redirect(url_for('index'))
    return render_template('register_donor.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('user_id'):
        flash('Please login first.', 'warning')
        return redirect(url_for('login'))
    conn = get_db_connection()
    donors = conn.execute('SELECT * FROM donor').fetchall()
    conn.close()
    return render_template('admin_dashboard.html', donors=donors)

if __name__ == '__main__':
    app.run(debug=True)
