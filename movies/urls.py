from django.urls import path
from . import views
app_name = "movies"

urlpatterns = [
    path("",views.movie_list,name = "movie_list"),
    path("<slug:slug>/shows",views.show_list,name = "show_list"),
    path("<slug:slug>/seats", views.seat_list,name = "seat_list"),
    # path("book/<slug:show_slug>/<int:seat_id>", views.book_seat,name = "book_seat"),
]
