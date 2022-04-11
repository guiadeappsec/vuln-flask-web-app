import sqlite3
import os
from util import get_root_dir


class DbHelper:

    def __init__(self) -> None:
        self.DB_FILE_PATH = f'{get_root_dir()}/temp/database.db'

        self.host = '10.0.0.99'
        self.port = 3306
        self.user = 'MyDbUser'
        self.password = 'M1DbPassword'


    def initialize(self):
        db_exists = os.path.exists(self.DB_FILE_PATH)

        if db_exists:
            return
        
        self._create_database()

    
    def execute_read(self, sql, params={}):
        con = None
        try:
            con = self._get_db_connection()
            cur = con.cursor()

            # cur.execute("select * from lang where first_appeared=:year", {"year": 1972})
            cur.execute(sql, params)
            result = cur.fetchall()

            return result

        finally:
            if con is not None:
                con.close()

    def execute_write(self, sql, params):
        con = None
        try:
            con = self._get_db_connection()
            cur = con.cursor()
            result = cur.execute(sql, params)
            con.commit()

            return result

        except Exception as err:
            if con is not None:
                con.rollback()
            
            raise err
        finally:
            if con is not None:
                con.close()

    
    def reset_database(self):
        os.remove(self.DB_FILE_PATH)
        self.initialize()


    def _create_database(self):
        con = None
        try:
            con = self._get_db_connection()
            cur = con.cursor()

            cur.execute('CREATE TABLE users (id integer, username text, password text, is_admin integer)')
            cur.execute('INSERT INTO users VALUES (1, "admin", "e64b78fc3bc91bcbc7dc232ba8ec59e0", 1)') # password: Admin123
            cur.execute('INSERT INTO users VALUES (2, "robso", "b3c634c91e1711c794704a031918a34b", 0)') # password: robso1980
            
            cur.execute('CREATE TABLE messages (message text)')
            cur.execute('INSERT INTO messages (message) VALUES ("This is vulnerable to stored xss")')
            
            cur.execute('CREATE TABLE products (id integer, name text, value real)')
            cur.execute('INSERT INTO products VALUES (1, "Uno", 9.99)')
            cur.execute('INSERT INTO products VALUES (2, "Sword", 749.50)')
            
            con.commit()
            con.close()
        finally:
            if con is not None:
                con.close()


    def _get_db_connection(self):
        return sqlite3.connect(self.DB_FILE_PATH)
        # return sqlite3.connect(':memory:')


db_helper = DbHelper()