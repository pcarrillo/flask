-- types definition

CREATE TABLE types (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	name_es TEXT,
	description TEXT,
	note TEXT,
	category_id INTEGER,
	parent_id INTEGER,
	CONSTRAINT category FOREIGN KEY (category_id) REFERENCES types(id),
	CONSTRAINT parent FOREIGN KEY (parent_id) REFERENCES types(id)
);

-- term definition

CREATE TABLE term (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	description TEXT,
	note TEXT,
	class_id INTEGER NOT NULL,
	type_id INTEGER NOT NULL,
	CONSTRAINT class FOREIGN KEY (class_id) REFERENCES types(id),
	CONSTRAINT "type" FOREIGN KEY (type_id) REFERENCES types(id)
);

-- triplets definition

CREATE TABLE triplets (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	description TEXT,
	note TEXT,
	subject_id INTEGER NOT NULL,
	predicate_id INTEGER NOT NULL,
	object_id INTEGER NOT NULL,
	CONSTRAINT subject FOREIGN KEY (subject_id) REFERENCES term(id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT predicate FOREIGN KEY (predicate_id) REFERENCES types(id) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT "object" FOREIGN KEY (object_id) REFERENCES term(id) ON DELETE CASCADE ON UPDATE CASCADE
);