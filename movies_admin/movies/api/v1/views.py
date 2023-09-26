
from rest_framework.generics import ListAPIView
from . import serializers
from ...models import Filmwork
import logging
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Count



class MoviesListAPIView(ListAPIView):

    serializer_class = serializers.FilmworkSerializer
    
    def get_queryset(self):
        logger = logging.basicConfig(level=logging.INFO, filename="views_new.log", filemode='w')
        logging.info("START")
        queryset = Filmwork.objects.all().prefetch_related('persons')
        annotated = queryset.filter(personfilmwork__role__icontains='actor').select_related('person').annotate(actors=ArrayAgg('person_full_name'))
        logging.info(annotated.query)
        return annotated