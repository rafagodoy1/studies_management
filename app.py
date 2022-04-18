import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
######################################## Connection functions ########################################
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

def get_contribution(contribution_id):
    conn = get_db_connection()
    contribution = conn.execute('SELECT * FROM contribution WHERE contribution_id = ?',
                        (contribution_id,)).fetchone()
    conn.close()
    if contribution is None:
        abort(404)
    return contribution

def get_reference(reference_id):
    conn = get_db_connection()
    reference = conn.execute('SELECT * FROM reference WHERE reference_id = ?',
                        (reference_id,)).fetchone()
    conn.close()
    if reference is None:
        abort(404)
    return reference

def get_interaction(interaction_id):
    conn = get_db_connection()
    interaction = conn.execute('SELECT * FROM interaction WHERE interaction_id = ?',
                        (interaction_id,)).fetchone()
    conn.close()
    if interaction is None:
        abort(404)
    return interaction

app = Flask(__name__)
app.config['SECRET_KEY'] = 'testlongstringaskey'
######################################## Metadata pages ########################################
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
######################################## KS pages ########################################
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

@app.route('/ks-<int:ks_id>/ks_edit', methods=('GET', 'POST'))
def ks_edit(ks_id):
    ks = get_ks(ks_id)

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

            sql_update = f"""UPDATE knowledge_source
                SET ks_type = '{ks_type}', 
                ks_name = '{ks_name}',
                main_person_id = {main_person_id},
                area = '{area}',
                greater_area = '{greater_area}'
                WHERE ks_id = {ks_id}"""
            
            conn.execute(sql_update)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('ks_edit.html', ks=ks)

@app.route('/ks-<int:ks_id>/ks_delete', methods=('POST',))
def ks_delete(ks_id):
    ks = get_ks(ks_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM knowledge_source WHERE ks_id = ?', (ks_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(ks['ks_name']))
    return redirect(url_for('index'))
######################################## Person pages ########################################
@app.route('/person-<int:person_id>')
def person(person_id):
    person = get_person(person_id)
    return render_template('person.html', person=person)

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

@app.route('/person-<int:person_id>/person_edit', methods=('GET', 'POST'))
def person_edit(person_id):
    person = get_person(person_id)

    if request.method == 'POST':
        person_name = request.form['person_name']

        if not person_name:
            flash('Name is required!')
        else:
            conn = get_db_connection()

            sql_update = f"""UPDATE person
                SET person_name = '{person_name}'
                WHERE person_id = {person_id}"""
            
            conn.execute(sql_update)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('person_edit.html', person=person)

@app.route('/person-<int:person_id>/person_delete', methods=('POST',))
def person_delete(person_id):
    person = get_person(person_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM person WHERE person_id = ?', (person_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(person['person_name']))
    return redirect(url_for('index'))
######################################## Reference pages ########################################
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

@app.route('/reference-<int:reference_id>/reference_edit', methods=('GET', 'POST'))
def reference_edit(reference_id):
    reference = get_reference(reference_id)

    if request.method == 'POST':
        ks_source_id = request.form['ks_source_id']
        ks_dependant_id = request.form['ks_dependant_id']
        is_mandatory = request.form['is_mandatory']
        dependency_source = request.form['dependency_source']

        if not ks_source_id:
            flash('KS Source ID is required!')
        elif not ks_dependant_id:
            flash('KS Dependancy ID is required!')
        elif not is_mandatory:
            flash('Is Mandatory Flag is required!')
        elif not dependency_source:
            flash('Dependency Source is required!')
        else:
            conn = get_db_connection()

            sql_update = f"""UPDATE reference
                SET ks_source_id = {ks_source_id},
                ks_dependant_id = {ks_dependant_id},
                is_mandatory = {is_mandatory},
                dependency_source = '{dependency_source}'
                WHERE reference_id = {reference_id}"""
            
            conn.execute(sql_update)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('reference_edit.html', reference=reference)

@app.route('/reference-<int:reference_id>/reference_delete', methods=('POST',))
def reference_delete(reference_id):
    reference = get_reference(reference_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM reference WHERE reference_id = ?', (reference_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(reference['reference_id']))
    return redirect(url_for('index'))

######################################## Contribution pages ########################################
@app.route('/contribution-<int:contribution_id>')
def contribution(contribution_id):
    contribution = get_contribution(contribution_id)
    return render_template('contribution.html', contribution=contribution)

@app.route('/contribution-list')
def contribution_list():
    
    conn = get_db_connection()
    contribution = conn.execute('SELECT * FROM contribution').fetchall()
    conn.close()

    return render_template('contribution_list.html', contribution=contribution)

@app.route('/contribution-create', methods=('GET', 'POST'))
def contribution_create():
    if request.method == 'POST':
        person_id = request.form['person_id']
        ks_id = request.form['ks_id']
        contribution_type = request.form['contribution_type']

        if not person_id:
            flash('Person ID is required!')
        elif not ks_id:
            flash('KS ID is required!')
        elif not contribution_type:
            flash('Contribution Type is required!')
        else:
            conn = get_db_connection()
            
            sql_insertion = f"INSERT INTO contribution (person_id, ks_id, contribution_type) VALUES ({person_id}, {ks_id}, '{contribution_type}')"
            conn.execute(sql_insertion)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('contribution_create.html')

@app.route('/contribution-<int:contribution_id>/contribution_edit', methods=('GET', 'POST'))
def contribution_edit(contribution_id):
    contribution = get_contribution(contribution_id)

    if request.method == 'POST':
        person_id = request.form['person_id']
        ks_id = request.form['ks_id']
        contribution_type = request.form['contribution_type']

        if not person_id:
            flash('Person ID is required!')
        elif not ks_id:
            flash('KS ID is required!')
        elif not contribution_type:
            flash('Contribution Type is required!')
        else:
            conn = get_db_connection()

            sql_update = f"""UPDATE contribution
                SET person_id = {person_id},
                ks_id = {ks_id},
                contribution_type = '{contribution_type}'
                WHERE contribution_id = {contribution_id}"""
            
            conn.execute(sql_update)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('contribution_edit.html', contribution=contribution)

@app.route('/contribution-<int:contribution_id>/contribution_delete', methods=('POST',))
def contribution_delete(contribution_id):
    contribution = get_contribution(contribution_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM contribution WHERE contribution_id = ?', (contribution_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(contribution['contribution_id']))
    return redirect(url_for('index'))
######################################## Interaction pages ########################################
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

@app.route('/interaction-<int:interaction_id>/interaction_edit', methods=('GET', 'POST'))
def interaction_edit(interaction_id):
    interaction = get_interaction(interaction_id)

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

            sql_update = f"""UPDATE interaction
                SET interaction_type_of_study = '{interaction_type_of_study}',
                ks_type = '{ks_type}',
                ks_id = {ks_id},
                ks_partition_type = '{ks_partition_type}',
                ks_partition_name = '{ks_partition_name}',
                ks_partition_number = '{ks_partition_number}',
                interaction_date = '{interaction_date}',
                ks_partition_metric = '{ks_partition_metric}',
                ks_partition_start = '{ks_partition_start}',
                ks_partition_finish = '{ks_partition_finish}',
                ks_partition_total = {ks_partition_total},
                ks_total = {ks_total},
                ks_partition_percentage = {ks_partition_percentage},
                interaction_log_type = '{interaction_log_type}',
                interaction_log_time_min = {interaction_log_time_min}
                WHERE interaction_id = {interaction_id}"""
            print(sql_update)
            conn.execute(sql_update)
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('interaction_edit.html', interaction=interaction)

@app.route('/interaction-<int:interaction_id>/interaction_delete', methods=('POST',))
def interaction_delete(interaction_id):
    interaction = get_interaction(interaction_id)
    conn = get_db_connection()
    conn.execute('DELETE FROM interaction WHERE interaction_id = ?', (interaction_id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(interaction['interaction_id']))
    return redirect(url_for('index'))