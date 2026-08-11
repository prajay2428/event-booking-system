from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
    path("movies/", views.MovieListView.as_view(), name= 'movie_list'),
    path("<slug:slug>/shows", views.ShowListView.as_view(), name = 'show_list'),
    path("<slug:slug>/seats",views.SeatListView.as_view(), name = "seat_list"),
]
