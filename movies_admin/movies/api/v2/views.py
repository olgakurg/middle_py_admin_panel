#from uu import Error
#from django.contrib.postgres.aggregates import ArrayAgg
from typing import Any
from django.db import models
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
#from django.db.models import Avg
import logging


from ...models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context) 

class MoviesListApi(MoviesApiMixin, BaseListView):
    fields = ('id', 'title', 'description')
      
    def get_queryset(self):
        filmworks =Filmwork.objects.prefetch_related('genres', 'persons').filter(title__icontains='Star Wars').all().values()
        return filmworks

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'results': list(self.get_queryset())}
        
        return context

    



class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_queryset(self):
        filmwork =Filmwork.objects.prefetch_related('genres', 'persons').filter(id = self.pk_url_kwarg).all().values()
        return filmwork

    def get_context_data(self, **kwargs):
        context = {
            'results': list(self.get_queryset())}
        return context
