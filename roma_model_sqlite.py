import sqlite3 as sqlite

#### COSAS POR IMPLEMENTAR #########

# Importación/Exportación de datos
# .import users.csv users
# .export users json users.json

# Resolver la verificación de la existencia de la BD y crearla si no existe
#  CREATE DATABASE IF NOT EXISTS web_analytics;


class rmDatos:
    def __init__(self):
        try:
            self.con = sqlite.connect(
                "data/roma_manual.db", autocommit=False, check_same_thread=False
            )
            self.con.execute("PRAGMA foreign_keys = ON;")
            self.cursor = self.con.cursor()
        except Exception as e:
            print(e)

    def getResults(self, sql):
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        self.con.commit()
        return results

    def getTypes(self):
        sql = "SELECT t.id, t.name as tipo, t2.name as clase  FROM types t JOIN types t2 on t.category_id = t2.id  order by t2.name, t.name ASC"
        return self.getResults(sql)

    def getTypeClasses(self):
        sql = "SELECT t2.id, t2.name  FROM types t JOIN types t2 on t.category_id = t2.id GROUP BY t2.name  order by t2.name, t.name ASC"
        return self.getResults(sql)

    def getTriplets(self):
        sql = "SELECT t.id, t2.name as subject, t3.name as predicate, t4.name as object, t.description, t.note  FROM triplets t JOIN term t2 on t.subject_id = t2.id  JOIN types t3 on t.predicate_id = t3.id JOIN term t4 on t.subject_id = t4.id"
        return self.getResults(sql)

    def getInstitutions(self):
        sql = "SELECT t.id , t.name as nombre  FROM term t JOIN types t2 on t.type_id = t2.id WHERE t2.name = 'rico:CorporateBody';"
        return self.getResults(sql)

    def db_init(self):
        sql = """
              CREATE TABLE types
              (
                  id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                  name        TEXT    NOT NULL,
                  name_es     TEXT,
                  description TEXT,
                  note        TEXT,
                  category_id INTEGER,
                  parent_id   INTEGER,
                  CONSTRAINT category FOREIGN KEY (category_id) REFERENCES types (id),
                  CONSTRAINT parent FOREIGN KEY (parent_id) REFERENCES types (id)
              );

              CREATE TABLE term
              (
                  id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                  name        TEXT    NOT NULL,
                  description TEXT,
                  note        TEXT,
                  class_id    INTEGER NOT NULL,
                  type_id     INTEGER NOT NULL,
                  CONSTRAINT class FOREIGN KEY (class_id) REFERENCES types (id),
                  CONSTRAINT "type" FOREIGN KEY (type_id) REFERENCES types (id)
              );

              CREATE TABLE triplets
              (
                  id           INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                  description  TEXT,
                  note         TEXT,
                  subject_id   INTEGER NOT NULL,
                  predicate_id INTEGER NOT NULL,
                  object_id    INTEGER NOT NULL,
                  CONSTRAINT subject FOREIGN KEY (subject_id) REFERENCES term (id) ON DELETE CASCADE ON UPDATE CASCADE,
                  CONSTRAINT predicate FOREIGN KEY (predicate_id) REFERENCES types (id) ON DELETE CASCADE ON UPDATE CASCADE,
                  CONSTRAINT "object" FOREIGN KEY (object_id) REFERENCES term (id) ON DELETE CASCADE ON UPDATE CASCADE
              );
              """
        try:
            self.cursor.execute(sql)
            self.con.commit()
            return True
        except Exception as e:
            print(e)
            return False
