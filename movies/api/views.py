from rest_framework import generics
from movies.api.serializers import MovieSerializer, ShowSerializer, SeatSerializer
from movies.models import Movie, Show, Seat,Theatre
from booking.models import BookingSeat,Booking
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ShowListView(generics.ListAPIView):
    serializer_class = ShowSerializer

    def get_queryset(self):
        slug = self.kwargs["slug"]
        return Show.objects.filter(movie__slug = slug)

class SeatListView(generics.ListAPIView):
    serializer_class = SeatSerializer

    def get_queryset(self):
        slug = self.kwargs["slug"]
        show = Show.objects.get(slug = slug)
        theatre = show.theatre
        return Seat.objects.filter(theatre = theatre)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        slug = self.kwargs["slug"]
        show = Show.objects.get(slug = slug)
        booked_seats = BookingSeat.objects.filter(show = show).values_list("seat_id",flat=True)
        context["booked_seats"] = booked_seats
        return context