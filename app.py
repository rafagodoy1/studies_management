import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_ks(ks_id):
    conn = get_db_connection()
    ks = conn.execute('SELECT * FROM knowledge_source WHERE ks_id = ?',
                        (ks_id,)).fetchone()
    conn.close()
    if ks is None:
        abort(404)
    return ks

def get_person(person_id):
    conn = get_db_connection()
    person = conn.execute('SELECT * FROM person WHERE person_id = ?',
                        (person_id,)).fetchone()
    conn.close()
    if person is None:
        abort(404)
    return person

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testlongstringaskey'

@app.route('/')
def index():
    conn = get_db_connection()
    knowledge_source = conn.execute('SELECT * FROM knowledge_source').fetchall()
    conn.close()
    return render_template('index.html', knowledge_source=knowledge_source)

@app.route('/about')
def about():
    conn = get_db_connection()

    return render_template('about.html')

@app.route('/ks-<int:ks_id>')
def ks(ks_id):
    ks = get_ks(ks_id)
    return render_template('ks.html', ks=ks)

@app.route('/ks-list')
def ks_list():
    
    conn = get_db_connection()
    knowledge_source = conn.execute('SELECT * FROM knowledge_source').fetchall()
    conn.close()

    return render_template('ks_list.html', knowledge_source=knowledge_source)

@app.route('/ks-create', methods=('GET', 'POST'))
def ks_create():

    if request.method == 'POST':
        ks_type = request.form['ks_type']
        ks_name = request.form['ks_name']
        main_person_id = request.form['main_person_id']
        area = request.form['area']
        greater_area = request.form['greater_area']

        if not ks_name:
            flash('Name is required!')
        elif not ks_type:
            flash('Type is required!')
        else:
            conn = get_db_connection()

            sql_insertion = 'INSERT INTO knowledge_source (ks_type, ks_name, main_person_id, area, greater_area)'
            sql_insertion = sql_insertion + f"VALUES ('{ks_type}','{ks_name}', {main_person_id},'{area}','{greater_area}');"
            
            conn.execute(sql_insertion)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('ks_create.html')

@app.route('/person-list')
def person_list():
    
    conn = get_db_connection()
    person = conn.execute('SELECT * FROM person').fetchall()
    conn.close()

    return render_template('person_list.html', person=person)

@app.route('/person-create', methods=('GET', 'POST'))
def person_create():
    if request.method == 'POST':
        person_name = request.form['person_name']

        if not person_name:
            flash('Name is required!')
        else:
            conn = get_db_connection()

            sql_insertion = f"INSERT INTO person (person_name) VALUES ('{person_name}')"
            
            conn.execute(sql_insertion)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('person_create.html')