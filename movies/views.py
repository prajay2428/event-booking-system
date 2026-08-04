from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from movies.models import Movie,Theatre,Seat,Show,Bookings
from cart.cart import Cart
# Create your views here.

def movie_list(request):
    movies = Movie.objects.all()
    return render(request,"movies/movie_list.html",{
        "movies" : movies
    })


def show_list(request,slug):
    shows = Show.objects.filter(movie__slug = slug)
    return render(request,"movies/show_list.html",{
        "shows" : shows
    })

def seat_list(request,slug):
    bookings = Bookings.objects.filter(show__slug = slug)
    booked_seats = bookings.values_list("seat_id",flat=True)
    show = get_object_or_404(Show,slug = slug)
    theatre = show.theatre
    seats = Seat.objects.filter(theatre = theatre)
    cart = Cart(request)
    seats_in_cart = []
    for item in cart:
        seats_in_cart.append(item["seat"])
    
    return render(request,"movies/seat_list.html",{
        "show" : show,
        "theatre" : theatre,
        "seats" : seats,
        "booked_seats" : booked_seats,
        "cart" : cart,
        "seats_in_cart" : seats_in_cart
    })
@login_required
def book_seat(request,seat_id,show_slug):
    seat = get_object_or_404(Seat,id = seat_id)
    show = get_object_or_404(Show,slug = show_slug)
    user = request.user
    booking = Bookings()
    booking.booked_by = user
    
    movie = show.movie
    theatre = show.theatre
    booking.movie = movie
    booking.theatre = theatre
    booking.seat = seat
    booking.show = show
    booking.save()
    messages.success("seat booked successfully")
    return render(
        request,
        "movies/book_seat.html",
        {"seat":seat,
         "show": show,
         "user":user,
         }

    )



    