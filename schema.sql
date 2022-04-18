DROP TABLE IF EXISTS knowledge_source;

CREATE TABLE knowledge_source (
	ks_id INTEGER PRIMARY KEY AUTOINCREMENT,
	ks_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	ks_type TEXT NOT NULL,
	ks_name TEXT NOT NULL,
	main_person_id INTEGER,
	area TEXT,
	greater_area TEXT
);

DROP TABLE IF EXISTS person;

CREATE TABLE person (
	person_id INTEGER PRIMARY KEY AUTOINCREMENT,
	person_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	person_name TEXT NOT NULL
);

CREATE TABLE reference (
	reference_id INTEGER PRIMARY KEY AUTOINCREMENT,
	reference_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	ks_source_id INTEGER NOT NULL,
	ks_dependant_id INTEGER NOT NULL,
	is_mandatory BOOLEAN NOT NULL,
	dependency_source TEXT NOT NULL
);