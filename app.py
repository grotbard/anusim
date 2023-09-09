from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['DATABASE'] = 'political_cause.db'

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            agree INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        agree = 1 if request.form.get('agree') else 0

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO candidates (full_name, email, phone, agree)
            VALUES (?, ?, ?, ?)
        ''', (full_name, email, phone, agree))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    return render_template('join.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        agree = 1 if request.form.get('agree') else 0

        # Debugging information
        print("Full Name:", full_name)
        print("Email:", email)
        print("Phone:", phone)
        print("Agree:", agree)

        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO candidates (full_name, email, phone, agree)
                VALUES (?, ?, ?, ?)
            ''', (full_name, email, phone, agree))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            conn.rollback()
            print("Error:", str(e))
            return 'Error occurred while adding the candidate to the database.'
@app.route('/candidates')
def candidates():
    conn = get_db_connection()
    candidates = conn.execute('SELECT * FROM candidates').fetchall()
    conn.close()
    return render_template('candidates.html', candidates=candidates)

if __name__ == '__main__':
    create_db_table()
    app.run(debug=True)
