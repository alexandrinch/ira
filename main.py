import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)


def create_database():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  sname TEXT,
                  grname TEXT,
                  sex TEXT,
                  day INTEGER)''')
    conn.commit()
    conn.close()


@app.route('/home')
@app.route('/')
def home_page():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    data = c.fetchall()
    conn.close()
    return render_template('home.html', data=data)


@app.route('/insert', methods=['GET', 'POST'])
def insert_page():
    if request.method == 'POST':
        name = request.form['name']
        sname = request.form['sname']
        grname = request.form['grname']
        sex = request.form['sex']
        day = request.form['day']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO students (name, sname, grname, sex, day) VALUES (?, ?, ?, ?, ?)',
                  (name, sname, grname, sex, day))
        conn.commit()
        conn.close()
    return render_template('insert.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_page():
    if request.method == 'POST':
        name = request.form['name']
        sname = request.form['sname']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('DELETE FROM students WHERE name=? AND sname=?', (name, sname))
        conn.commit()
        conn.close()
    return render_template('delete.html')


@app.route('/select', methods=['GET', 'POST'])
def select_page():
    if request.method == 'POST':
        grname = request.form['grname']
        order_by = request.form.get('order_by')
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        query = 'SELECT name, sname FROM students WHERE grname=?'
        if order_by:
            query += f' ORDER BY sname {order_by}'
        else:
            query += f' ORDER BY sname {order_by}'
        c.execute(query, (grname,))
        data = c.fetchall()
        conn.close()
        return render_template('select.html', data=data)
    return render_template('select.html')


@app.route('/select_age', methods=['GET', 'POST'])
def select_age_page():
    if request.method == 'POST':
        sex = request.form['sex']
        more_than = request.form['more_than']
        order_by = request.form.get('order_by')
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        query = c.execute(f'''SELECT name,sname,grname 
                            FROM students 
                            WHERE sex='{sex}' AND day>'{more_than}' 
                            ORDER BY grname {order_by}, sname {order_by};
                            ''')
        data = query.fetchall()
        conn.close()
        return render_template('select_age.html', data=data)
    return render_template('select_age.html')


@app.route('/create', methods=['POST'])
def create_page():
    if request.method == 'POST':
        create_database()

if __name__ == '__main__':
    app.run()
