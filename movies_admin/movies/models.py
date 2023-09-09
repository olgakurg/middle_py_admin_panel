import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True

class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        
        abstract = True
        
class Genre(UUIDMixin, TimeStampedMixin):
    # Первым аргументом обычно идёт человекочитаемое название поля
    name = models.CharField('name', max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField('description', blank=True)

    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"genre"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры' 

    def __str__(self):
        return self.name
    
class Person(UUIDMixin, TimeStampedMixin):
    # Первым аргументом обычно идёт человекочитаемое название поля
    full_name = models.TextField('full_name')
    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"person"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники' 

    def __str__(self):
        return self.full_name

class Filmwork(UUIDMixin, TimeStampedMixin):
  
    title = models.CharField('name', max_length=255)
    description = models.TextField('description', blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    class TypeOfFilm(models.TextChoices):
        MOVIE = 'MV', _('Movie')
        TV_SHOW = 'SH', _('TV Show')

    type_of_film = models.CharField(
        max_length=2,
        choices=TypeOfFilm.choices,
        default=TypeOfFilm.MOVIE,
    )

    def is_upperclass(self):
        return self.type_of_film in {
            self.type_of_film.MOVIE,
            self.type_of_film.TV_SHOW,
        } 
            
    rating = models.FloatField('rating', blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)]) 
    
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    
    class Meta:
        # Ваши таблицы находятся в нестандартной схеме. Это нужно указать в классе модели
        db_table = "content\".\"film_work"
        # Следующие два поля отвечают за название модели в интерфейсе
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title 

class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work" 

class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField('role', null=True)
    created = models.DateTimeField(auto_now_add=True) 