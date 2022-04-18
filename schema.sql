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

DROP TABLE IF EXISTS reference;

CREATE TABLE reference (
	reference_id INTEGER PRIMARY KEY AUTOINCREMENT,
	reference_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	ks_source_id INTEGER NOT NULL,
	ks_dependant_id INTEGER NOT NULL,
	is_mandatory BOOLEAN NOT NULL,
	dependency_source TEXT NOT NULL
);

DROP TABLE IF EXISTS contribution;

CREATE TABLE contribution (
	contribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
	contribution_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	person_id INTEGER NOT NULL,
	ks_id INTEGER NOT NULL,
	contribution_type TEXT NOT NULL
);

DROP TABLE IF EXISTS interaction;

CREATE TABLE interaction (
	interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
	interaction_created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	interaction_type_of_study TEXT NOT NULL,
	ks_type TEXT NOT NULL,
	ks_id INTEGER NOT NULL,
	ks_partition_type TEXT NOT NULL,
	ks_partition_name TEXT NOT NULL,
	ks_partition_number TEXT NOT NULL,
	interaction_date TIMESTAMP NOT NULL,
	ks_partition_metric TEXT NOT NULL,
	ks_partition_start TEXT NOT NULL,
	ks_partition_finish TEXT NOT NULL,
	ks_partition_total INTEGER NOT NULL,
	ks_total INTEGER NOT NULL,
	ks_partition_percentage NUMBER NOT NULL,
	interaction_log_type TEXT NOT NULL,
	interaction_log_time_min INTEGER NOT NULL
);