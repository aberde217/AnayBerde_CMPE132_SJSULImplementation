from flask import Flask, render_template, request, flash, redirect, url_for, session
import sqlite3
import hashlib
import secrets
app = Flask(__name__)
app.secret_key = "waFEZ3cLWaeQZr1fr5yqULit"

def get_db_connection():
    conn = sqlite3.connect('mlklibrary.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form['library_id']
        plaintext = request.form['password']

        conn = sqlite3.connect('mlklibrary.db') # connect route to database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE library_id = (?)", (id,)) # selects ROW for that library id if it exists
        row = cursor.fetchone()
        session['first_name'] = row[0] # used for role-based pages
        if row is None:
            flash('Invalid Credentials, login failed.', 'error')
        else:
            salt = row[6] # last column, which is salt
            hash_obj = hashlib.sha256((salt + plaintext).encode())
            hash_val = hash_obj.hexdigest()
            if hash_val != row[3]: # compare entered password with stored (hashed/salted)
                flash('Invalid Credentials, login failed', 'error')
            elif row[5] == 'inactive':  # check if user is active
                flash('Account deactivated. Visit MLK Library for further action.', 'error')
            else:
                role = row[4]
                if role == "Librarian":
                    return redirect(url_for('dashboard'))
                elif role == "Student":
                    return redirect(url_for('student'))
                elif role == "Professor":
                    return redirect(url_for('professor'))
                else:
                    return redirect(url_for('borrower'))
    return render_template('login.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        id = request.form['library_id']
        cursor.execute("UPDATE Users SET active_status = 'inactive' WHERE library_id = (?)", (id,))
        conn.commit()
    rows = conn.execute(
        "SELECT first_name || ' ' || last_name AS full_name, library_id, role FROM Users WHERE active_status = 'active'"
    ).fetchall()
    conn.close()

    users = [dict(row) for row in rows]

    return render_template('admin_dashboard.html', users=users)

@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        session.clear() # clears session data,
        return redirect(url_for('login'))
    return render_template('student_page.html')

@app.route('/professor', methods=['GET', 'POST'])
def professor():
    if request.method == 'POST':
        session.clear() # clears session data,
        return redirect(url_for('login'))
    return render_template('student_page.html')

@app.route('/borrower', methods=['GET', 'POST'])
def borrower():
    if request.method == 'POST':
        session.clear() # clears session data,
        return redirect(url_for('login'))
    return render_template('borrower_page.html')

@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        library_id = request.form['library_id']
        role = request.form['role']

        plaintext = request.form['password']
        salt = secrets.token_hex(8)
        temp = hashlib.sha256((salt + plaintext).encode())
        hashed_password = temp.hexdigest()
        conn = sqlite3.connect('mlklibrary.db') # connect route to database
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?)"""
        ,(first_name, last_name, library_id, hashed_password, role, "active", salt)) # insert user-defined variables into database
        conn.commit()
        conn.close()
    return render_template('create_user.html')

if __name__ == '__main__':
    app.run(debug=True)