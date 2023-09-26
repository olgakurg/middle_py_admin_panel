from models import Genre, Filmwork


def get_movies():
    star_wars_films = Filmwork.objects.prefetch_related('genres', 'persons').filter(title__icontains='Star Wars')[:10]
    for filmwork in star_wars_films:
        print(filmwork.genres.all())
        print(filmwork.persons.filter(full_name='Robert')) 