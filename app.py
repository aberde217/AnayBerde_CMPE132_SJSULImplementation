from flask import Flask, render_template, request, flash
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
                conn = get_db_connection()
                rows = conn.execute(
                    "SELECT first_name || ' ' || last_name AS full_name, library_id, role FROM Users"
                ).fetchall()
                conn.close()

                users = [dict(row) for row in rows]
                return render_template('admin_dashboard.html', users=users)
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT first_name || ' ' || last_name AS full_name, library_id, role FROM Users"
    ).fetchall()
    conn.close()

    users = [dict(row) for row in rows]

    return render_template('admin_dashboard.html', users=users)

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