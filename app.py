from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "dbname=my_app user=postgres password=root host=localhost"
)

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM records ORDER BY id;')
    records = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/record/<int:id>')
def record(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM records WHERE id = %s;', (id,))
    record = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('detail.html', record=record)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO records (name, email, phone) VALUES (%s, %s, %s);',
                    (name, email, phone))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur.execute('UPDATE records SET name=%s, email=%s, phone=%s WHERE id=%s;',
                    (name, email, phone, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))
    else:
        cur.execute('SELECT * FROM records WHERE id=%s;', (id,))
        record = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('edit.html', record=record)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM records WHERE id=%s;', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
