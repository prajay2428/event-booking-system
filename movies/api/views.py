from rest_framework import generics
from movies.api.serializers import MovieSerializer, ShowSerializer
from movies.models import Movie, Show

class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ShowListView(generics.ListAPIView):
    serializer_class = ShowSerializer

    def get_queryset(self):
        slug = self.kwargs["slug"]
        return Show.objects.filter(movie__slug = slug)