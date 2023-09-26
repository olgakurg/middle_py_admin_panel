from http import server
from ... import models
from rest_framework import serializers

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = ('full_name',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('name')
                
class StringListSerializer(serializers.ListSerializer):
    child = serializers.CharField()        

class FilmworkSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    #actors = serializers.FloatField()
    actors = StringListSerializer()
    #directors = StringListSerializer()
    #writers = StringListSerializer()

    class Meta:
        model = models.Filmwork
        #fields = ('id', 'title', 'description', 'created', 'type', 'genres', 'actors', 'directors', 'writers')
        fields = ('id', 'title', 'description', 'created', 'type', 'genres', 'actors')
        depth = 3
