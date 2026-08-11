# booking/api/urls.py

from django.urls import path
from .views import BookingCreateView, MyBookingsView


urlpatterns = [
    path(
        "create/",
        BookingCreateView.as_view(),
        name="booking_create"
    ),

    path(
        "my-bookings/",
        MyBookingsView.as_view(),
        name="my_bookings"
    ),
]