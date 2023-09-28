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
    creation_date = serializers.CharField(source = 'created')
    genres = serializers.StringRelatedField(many=True)
    actors = StringListSerializer()
    directors = StringListSerializer()
    writers = StringListSerializer()


    class Meta:
        model = models.Filmwork
        fields = ('id', 'title', 'description', 'creation_date', 'type', 'genres', 'actors', 'directors', 'writers')
        depth = 3
