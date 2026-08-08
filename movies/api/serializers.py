from rest_framework import serializers
from movies.models import Movie, Show

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title','slug','poster','description','director','release_date']


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ['movie','theatre','date','time','slug']