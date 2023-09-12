import sqlite3

import psycopg2

from dataclasses import astuple
from data_classes import Genre, Person, GenreFilmwork, PersonFilmwork, Filmwork
from settings import dsl, db_path, table_to_dataclass, TABLE_COLUMNS_NAME


from contextlib import contextmanager  
import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn 
    conn.close() 


class SQLiteExtractor():

    def __init__(self, conn):
        self.conn = conn
     
    def extract_to_dataclasses(self, table_name):
        conn = self.conn
        conn.row_factory = sqlite3.Row  
        curs = conn.cursor()
        try:
            curs.execute(f"SELECT * FROM {table_name};")
        except sqlite3.Error as err:
                logging.error(err)
                
        results = curs.fetchall()
        lst = []
        class_name = table_to_dataclass[table_name]
        for result in results:
            obj = globals()[class_name]
            lst.append(obj(**dict(result)))
        return lst   
    
class PostgresSaver():
    def __init__(self, conn):
        self.conn = conn
    
    def insert_data(self, data, table_name):
        conn = self.conn
        column_names = TABLE_COLUMNS_NAME[table_name]
        col_count = ', '.join(['%s'] * len(column_names)) 
        items = [astuple(item) for item in data]
        with conn.cursor() as cursor:
            args = ', '.join(cursor.mogrify(f"{col_count}", item).decode('utf-8') for item in items)
            column_names = ', '.join(column_names)
            query = f"""
                    INSERT INTO content.{table_name} ({column_names}) 
                    VALUES {args}
                    ON CONFLICT (id) DO NOTHING;
                    """
            try: 
                cursor.execute(query)
            except psycopg2.Error as err:
                logging.error(err)
            
 
def load_from_sqlite(connection, pg_conn):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)
    for table_name in table_to_dataclass:
        data = sqlite_extractor.extract_to_dataclasses(table_name)
        postgres_saver.insert_data(data, table_name)


if __name__ == '__main__':
   
    with conn_context(db_path) as sqlite_conn, psycopg2.connect(**dsl) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
