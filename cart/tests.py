from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from booking.models import Booking, BookingSeat
from movies.models import Movie, Seat, Show, Theatre


class CartApiTests(TestCase):
    def setUp(self):
        self.theatre = Theatre.objects.create(name="Main", address="One Street")
        self.other_theatre = Theatre.objects.create(name="Other", address="Two Street")
        self.movie = Movie.objects.create(
            title="Test Movie", director="Director", release_date=timezone.now()
        )
        self.show = Show.objects.create(
            movie=self.movie,
            theatre=self.theatre,
            date=timezone.localdate(),
            time="18:00",
        )
        self.seat = Seat.objects.create(
            theatre=self.theatre,
            name="A1",
            price=Decimal("250.00"),
            category=Seat.Category.GOLD,
        )
        self.other_seat = Seat.objects.create(
            theatre=self.other_theatre,
            name="Z1",
            price=Decimal("300.00"),
            category=Seat.Category.PREMIUM,
        )

    def test_cart_returns_show_total_and_seat_id(self):
        response = self.client.post(f"/api/cart/add/{self.seat.id}/{self.show.id}")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/api/cart/")
        self.assertEqual(response.data["show"]["id"], self.show.id)
        self.assertEqual(response.data["items"][0]["seat"]["id"], self.seat.id)
        self.assertEqual(response.data["total"], Decimal("250.00"))

    def test_seat_from_another_theatre_is_rejected(self):
        response = self.client.post(
            f"/api/cart/add/{self.other_seat.id}/{self.show.id}"
        )
        self.assertEqual(response.status_code, 409)

    def test_booked_seat_is_rejected(self):
        user = get_user_model().objects.create_user("booker", password="password")
        booking = Booking.objects.create(
            user=user,
            first_name="Test",
            last_name="User",
            email="test@example.com",
            show=self.show,
            total_amount=self.seat.price,
            payment_status=Booking.PaymentStatus.PAID,
        )
        BookingSeat.objects.create(
            booking=booking,
            seat=self.seat,
            show=self.show,
            price_paid=self.seat.price,
        )

        response = self.client.post(f"/api/cart/add/{self.seat.id}/{self.show.id}")
        self.assertEqual(response.status_code, 409)
