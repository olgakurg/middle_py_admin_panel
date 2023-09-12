import sqlite3
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

import uuid
from dataclasses import dataclass, astuple
from datetime import datetime

from contextlib import contextmanager  
import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn # С конструкцией yield вы познакомитесь в следующем модуле 
    # Пока воспринимайте её как return, после которого код может продолжить выполняться дальше
    conn.close() 


@dataclass(frozen=True)
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

table_to_dataclass = {
     'genre' : 'Genre',
     'person' : 'Person',
     'film_work' : 'Filmwork',
     'person_film_work' : 'PersonFilmwork',
     'genre_film_worl' : 'GenreFilmwork',
}

class SQLiteExtractor():

    def __init__(self, conn):
        self.conn = conn
     
    def extract_to_dataclasses(self, table_name):
        conn = self.conn
        conn.row_factory = sqlite3.Row  
        curs = conn.cursor()
        table_name = 'genre'
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
    
    def exract_genres(self):
        genres = self.extract_to_dataclasses('genres')
        return genres

class PostgresSaver():
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
    
    def save_genres(self, data):
        
        table_name  = 'genre'
        column_names = (
            'id',
            'name',
            'description',
            'created',
            'modified',
        )

        col_count = ', '.join(['%s'] * len(column_names)) 
        cursor = self.cursor
        
        item = data[0]
        args = ','.join(cursor.mogrify(f"({col_count})", row).decode('utf-8') for row in astuple(item))
        
        query = f"""
                       INSERT INTO content.{table_name} {column_names} 
                       VALUES {args}
                       ON CONFLICT (id) DO NOTHING;
                    """
            
        #cursor.execute(query)
        print (query)

        

#метод-последовательсность - genre, person, film_work, personfilmwork, genrefilmwork.

def load_from_sqlite(connection: sqlite3.Connection): #, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn, cursor)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.exract_genres()
    postgres_saver.save_genres(data)

if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}   
    db_path = 'db.sqlite'
    
    with conn_context(db_path) as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn, pg_conn.cursor as cursor:
        load_from_sqlite(sqlite_conn, pg_conn, cursor)
