dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}   
db_path = 'db.sqlite'

BATCH_SIZE  = 1000

TABLE_COLUMNS_NAME = {
          'person_film_work':
          (
            'id',
            'person_id',
            'film_work_id',
            'role',
            'created',
        ),
        'genre_film_work':
        (
            'id',
            'genre_id',
            'film_work_id',
            'created',
        ),
         'film_work':
        (
            'id',
            'title',
            'description',
            'creation_date',
            'file_path',  
            'rating',
            'type',
            'created',
            'modified',
        ),
        'person':
        (
            'id',
            'full_name',
            'created',
            'modified',
        ),
        'genre':
        (
            'id',
            'name',
            'description',
            'created',
            'modified',
        ),
}
