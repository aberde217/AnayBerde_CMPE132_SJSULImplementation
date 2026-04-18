from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('mlklibrary.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/dashboard')
def dashboard():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT first_name || ' ' || last_name AS full_name, library_id, role FROM users"
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
        password = request.form['password']
        role = request.form['role']

        conn = sqlite3.connect('mlklibrary.db') # connect route to database
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO Users (first_name, last_name, library_id, password, role) VALUES (?, ?, ?, ?, ?)"""
                       ,(first_name, last_name, library_id, password, role)) # insert user-defined variables into database
        conn.commit()
        conn.close()
    return render_template('create_user.html')

if __name__ == '__main__':
    app.run(debug=True)