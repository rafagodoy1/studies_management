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

@app.route('/reference-list')
def reference_list():
    
    conn = get_db_connection()
    reference = conn.execute('SELECT * FROM reference').fetchall()
    conn.close()

    return render_template('reference_list.html', reference=reference)

@app.route('/reference-create', methods=('GET', 'POST'))
def reference_create():
    if request.method == 'POST':
        ks_source_id = request.form['ks_source_id']
        ks_dependant_id = request.form['ks_dependant_id']
        is_mandatory = request.form['is_mandatory']
        dependency_source = request.form['dependency_source']

        if not ks_source_id:
            flash('KS Source ID is required!')
        elif not ks_dependant_id:
            flash('KS Dependant ID is required!')
        elif not is_mandatory:
            flash('Is Mandatory Flag is required!')
        elif not dependency_source:
            flash('Dependancy Source is required!')
        else:
            conn = get_db_connection()
            
            sql_insertion = "INSERT INTO reference (ks_source_id, ks_dependant_id, is_mandatory, dependency_source) VALUES "
            sql_insertion = sql_insertion + f"({ks_source_id}, {ks_dependant_id}, {is_mandatory}, '{dependency_source}')"
            conn.execute(sql_insertion)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('reference_create.html')

@app.route('/interaction-list')
def interaction_list():
    
    conn = get_db_connection()
    interaction = conn.execute('SELECT * FROM interaction').fetchall()
    conn.close()

    return render_template('interaction_list.html', interaction=interaction)

@app.route('/interaction-create', methods=('GET', 'POST'))
def interaction_create():
    if request.method == 'POST':
        interaction_type_of_study = request.form['interaction_type_of_study']
        ks_type = request.form['ks_type']
        ks_id = request.form['ks_id']
        ks_partition_type = request.form['ks_partition_type']
        ks_partition_name = request.form['ks_partition_name']
        ks_partition_number = request.form['ks_partition_number']
        interaction_date = request.form['interaction_date']
        ks_partition_metric = request.form['ks_partition_metric']
        ks_partition_start = request.form['ks_partition_start']
        ks_partition_finish = request.form['ks_partition_finish']
        ks_partition_total = request.form['ks_partition_total']
        ks_total = request.form['ks_total']
        ks_partition_percentage = request.form['ks_partition_percentage']
        interaction_log_type = request.form['interaction_log_type']
        interaction_log_time_min = request.form['interaction_log_time_min']

        if not ks_type:
            flash('KS Type is required!')
        elif not ks_id:
            flash('KS ID is required!')
        elif not ks_partition_type:
            flash('Partition Type is required!')
        elif not ks_partition_name:
            flash('Partition Name is required!')
        elif not ks_partition_number:
            flash('Partition NUmber is required!')
        elif not interaction_date:
            flash('Study Date is required!')
        elif not ks_partition_metric:
            flash('Partition Metric is required!')
        elif not ks_partition_start:
            flash('Partition Start is required!')
        elif not ks_partition_finish:
            flash('Partition Finish is required!')
        elif not ks_partition_total:
            flash('Partition Total is required!')
        elif not ks_total:
            flash('KS Total is required!')
        elif not ks_partition_percentage:
            flash('Partition Percentage is required!')
        elif not interaction_log_type:
            flash('Log Type is required!')
        elif not interaction_log_time_min:
            flash('Log Time is required!')
        else:
            conn = get_db_connection()

            sql_insertion = f"""INSERT INTO interaction (
                interaction_type_of_study,
                ks_type,
                ks_id,
                ks_partition_type,
                ks_partition_name,
                ks_partition_number,
                interaction_date,
                ks_partition_metric,
                ks_partition_start,
                ks_partition_finish,
                ks_partition_total,
                ks_total,
                ks_partition_percentage,
                interaction_log_type,
                interaction_log_time_min
            ) VALUES (
                '{interaction_type_of_study}',
                '{ks_type}',
                {ks_id},
                '{ks_partition_type}',
                '{ks_partition_name}',
                '{ks_partition_number}',
                '{interaction_date}',
                '{ks_partition_metric}',
                '{ks_partition_start}',
                '{ks_partition_finish}',
                {ks_partition_total},
                {ks_total},
                {ks_partition_percentage},
                '{interaction_log_type}',
                {interaction_log_time_min}
            );"""
            conn.execute(sql_insertion)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('interaction_create.html')