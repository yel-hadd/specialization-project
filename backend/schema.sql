-- EduTrack Analytics - schema PostgreSQL

CREATE TABLE classes (
	id SERIAL NOT NULL, 
	name VARCHAR(120) NOT NULL, 
	level VARCHAR(80), 
	academic_year VARCHAR(20), 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_classes_name ON classes (name);

CREATE TABLE imports (
	id SERIAL NOT NULL, 
	filename VARCHAR(255) NOT NULL, 
	type VARCHAR(40) NOT NULL, 
	imported_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	rows_processed INTEGER NOT NULL, 
	rows_rejected INTEGER NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	error_log TEXT, 
	PRIMARY KEY (id)
);

CREATE TABLE modules (
	id SERIAL NOT NULL, 
	code VARCHAR(40) NOT NULL, 
	name VARCHAR(160) NOT NULL, 
	coefficient FLOAT NOT NULL, 
	ects INTEGER, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_modules_code ON modules (code);

CREATE TABLE settings (
	id SERIAL NOT NULL, 
	key VARCHAR(80) NOT NULL, 
	value FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_settings_key UNIQUE (key)
);
CREATE INDEX ix_settings_key ON settings (key);

CREATE TABLE users (
	id SERIAL NOT NULL, 
	email VARCHAR(255) NOT NULL, 
	hashed_password VARCHAR(255) NOT NULL, 
	role VARCHAR(50) NOT NULL, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE TABLE students (
	id SERIAL NOT NULL, 
	student_code VARCHAR(40) NOT NULL, 
	first_name VARCHAR(120) NOT NULL, 
	last_name VARCHAR(120) NOT NULL, 
	email VARCHAR(255), 
	class_id INTEGER, 
	enrollment_date DATE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(class_id) REFERENCES classes (id) ON DELETE SET NULL
);
CREATE INDEX ix_students_class_id ON students (class_id);
CREATE UNIQUE INDEX ix_students_student_code ON students (student_code);

CREATE TABLE absences (
	id SERIAL NOT NULL, 
	student_id INTEGER NOT NULL, 
	module_id INTEGER, 
	date DATE, 
	hours FLOAT NOT NULL, 
	type VARCHAR(20) NOT NULL, 
	justified BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(student_id) REFERENCES students (id) ON DELETE CASCADE, 
	FOREIGN KEY(module_id) REFERENCES modules (id) ON DELETE SET NULL
);
CREATE INDEX ix_absences_module_id ON absences (module_id);
CREATE INDEX ix_absences_student_id ON absences (student_id);

CREATE TABLE alerts (
	id SERIAL NOT NULL, 
	student_id INTEGER NOT NULL, 
	alert_type VARCHAR(40) NOT NULL, 
	severity VARCHAR(20) NOT NULL, 
	message TEXT NOT NULL, 
	threshold_value FLOAT, 
	metric_value FLOAT, 
	created_at TIMESTAMP WITH TIME ZONE NOT NULL, 
	resolved BOOLEAN NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(student_id) REFERENCES students (id) ON DELETE CASCADE
);
CREATE INDEX ix_alerts_student_id ON alerts (student_id);

CREATE TABLE grades (
	id SERIAL NOT NULL, 
	student_id INTEGER NOT NULL, 
	module_id INTEGER NOT NULL, 
	value FLOAT NOT NULL, 
	assessment_type VARCHAR(60), 
	period VARCHAR(40), 
	date DATE, 
	PRIMARY KEY (id), 
	FOREIGN KEY(student_id) REFERENCES students (id) ON DELETE CASCADE, 
	FOREIGN KEY(module_id) REFERENCES modules (id) ON DELETE CASCADE
);
CREATE INDEX ix_grades_module_id ON grades (module_id);
CREATE INDEX ix_grades_period ON grades (period);
CREATE INDEX ix_grades_student_id ON grades (student_id);
