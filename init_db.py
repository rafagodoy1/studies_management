import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

sql_query = """
    INSERT INTO knowledge_source (ks_id, ks_created_at, ks_type, ks_name, main_person_id, area, greater_area)
    VALUES
        (1,'2022-04-17 23:00:00','Book','A liberdade eh uma luta constante',1,'Ativismo','Politica'),
        (2,'2022-04-18 11:00:00','Book','Apontamentos sobre a teoria do autoritarismo',2,'Teoria econômica e política','Sociologia'),
        (3,'2022-04-18 11:00:00','Book','Ligações perigosas: casamentos e divórcios entre o marxismo e o feminismo',3,'Feminismo','Politica'),
        (4,'2022-04-18 11:00:00','Book','Ensinando pensamento crítico',4,'Educação','Comunicação'),
        (5,'2022-04-18 11:00:00','Book','Discurso sobre o colonialismo',5,'Colonialismo','Politica'),
        (6,'2022-04-18 11:00:00','Book','Ideias para a luta',6,'Ativismo','Politica');
"""

cur.execute(sql_query)

sql_query = """
    INSERT INTO person (person_id, person_created_at, person_name)
    VALUES
        (1,'2022-04-18 11:00:00','Angela Davis'),
        (2,'2022-04-18 11:00:00','Florestan Fernandes'),
        (3,'2022-04-18 11:00:00','Cinzia Arruzza'),
        (4,'2022-04-18 11:00:00','bell hooks'),
        (5,'2022-04-18 11:00:00','Aimé Césaire'),
        (6,'2022-04-18 11:00:00','Marta Harnecker');
"""

cur.execute(sql_query)

sql_query = """
    INSERT INTO reference (reference_id, reference_created_at, ks_source_id, ks_dependant_id, is_mandatory, dependency_source)
    VALUES
        (1, '2022-04-18 11:00:00', 1, 2, True, 'Fundamentes Ciclo'),
        (2, '2022-04-18 11:00:00', 2, 3, True, 'Fundamentes Ciclo'),
        (3, '2022-04-18 11:00:00', 3, 4, True, 'Fundamentes Ciclo'),
        (4, '2022-04-18 11:00:00', 4, 5, True, 'Fundamentes Ciclo'),
        (5, '2022-04-18 11:00:00', 5, 6, True, 'Fundamentes Ciclo');
"""

cur.execute(sql_query)

connection.commit()
connection.close()