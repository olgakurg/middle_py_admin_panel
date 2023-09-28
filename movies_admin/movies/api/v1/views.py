
from rest_framework.generics import ListAPIView, RetrieveAPIView
from . import serializers
from ...models import Filmwork, Person, PersonFilmwork
import logging
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg


class MoviesAPIMixin():

    serializer_class = serializers.FilmworkSerializer
    
    def get_queryset(self):
        logging.basicConfig(level=logging.INFO, filename="views_new.log", filemode='w')
        logging.info("START LIST VIEW")
        queryset = Filmwork.objects.all()
        films = (
            queryset.prefetch_related("persons")
            .annotate(
                actors=ArrayAgg(
                "personfilmwork__person__full_name", 
                filter=Q(personfilmwork__role="actor")
                )
            )
            .annotate(
                directors=ArrayAgg(
                "personfilmwork__person__full_name", 
                filter=Q(personfilmwork__role="director"),
                )
             )
            .annotate(
                writers=ArrayAgg(
                "personfilmwork__person__full_name", 
                filter=Q(personfilmwork__role="writer"),
                )
             )
            .select_related()
        )
        logging.info(films.query)
        return films
    
class MoviesListAPIView(MoviesAPIMixin, ListAPIView):
    pass
    
class MoviesDetailApi(MoviesAPIMixin, RetrieveAPIView):
    pass