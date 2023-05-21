import sqlite3

from my_web_fw.mini_orm.exceptions import DbExecutescriptError, DbCommitError


class SQLLite:
    def __init__(self, name: str):
        self.name = name if name.find(".sqlite") != -1 else "{}.sqlite".format(name)

    @property
    def connect(self):
        with sqlite3.connect(self.name) as connect:
            return connect

    @property
    def cursor(self):
        return self.connect.cursor()

    def __commit(self):
        try:
            self.connect.commit()
        except Exception as e:
            raise DbCommitError(e.args)

    def executescript(self, script: str):
        script = script.replace("BEGIN TRANSACTION;", "").replace("COMMIT TRANSACTION;", "")
        script = "BEGIN TRANSACTION;\n\r{}\n\rCOMMIT TRANSACTION;".format(script)
        # try:
        self.cursor.executescript(script)
        # except Exception as e:
        #     raise DbExecutescriptError(e.args)

    def insert(self, obj, table_name: str = None):
        table_name = obj.__class__.__name__ if table_name is None else table_name
        statement = "INSERT INTO {} (?) VALUES (?)".format(table_name)
        self.cursor.execute(statement, (tuple(vars(obj).keys()), tuple(vars(obj).values())))
        self.__commit()

    # def update(self, obj, up, table_name: str = None):
    #     table_name = obj.__class__.__name__ if table_name is None else table_name
    #     statement = f"UPDATE {table_name} SET name=? WHERE id=?"
    #
    #     self.cursor.execute(statement, (obj.name, obj.id))
    #     try:
    #         self.connection.commit()
    #     except Exception as e:
    #         raise DbUpdateException(e.args)
    #
    # def delete(self, obj):
    #     statement = f"DELETE FROM {self.tablename} WHERE id=?"
    #     self.cursor.execute(statement, (obj.id,))
    #     try:
    #         self.connection.commit()
    #     except Exception as e:
    #         raise DbDeleteException(e.args)
    #
    # def find_by_id(self, id):
    #     statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
    #     self.cursor.execute(statement, (id,))
    #     result = self.cursor.fetchone()
    #     if result:
    #         return Student(*result)
    #     else:
    #         raise RecordNotFoundException(f'record with id={id} not found')

SCRIPT = "BEGIN TRANSACTION;\n\r" \
         "DROP TABLE IF EXISTS Sad;\n\r" \
         "CREATE TABLE Sad (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32));\n\r" \
         "COMMIT TRANSACTION;"

s = SQLLite("test")
s.executescript(SCRIPT)

class Sad:
    def __init__(self):
        self.name = "sda"

    def lol(self):
        pass

sad = Sad()

s.insert(sad)
