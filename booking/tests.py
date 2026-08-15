from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from movies.models import Movie, Seat, Show, Theatre
from .models import Booking


class BookingApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "buyer", email="buyer@example.com", password="password"
        )
        theatre = Theatre.objects.create(name="Main", address="One Street")
        movie = Movie.objects.create(
            title="Test Movie", director="Director", release_date=timezone.now()
        )
        self.show = Show.objects.create(
            movie=movie,
            theatre=theatre,
            date=timezone.localdate(),
            time="18:00",
        )
        self.seat = Seat.objects.create(
            theatre=theatre,
            name="A1",
            price=Decimal("250.00"),
            category=Seat.Category.GOLD,
        )
        self.client.force_login(self.user)

    def test_booking_uses_calculated_total_and_is_paid(self):
        self.client.post(f"/api/cart/add/{self.seat.id}/{self.show.id}")
        response = self.client.post(
            "/api/booking/create/",
            {
                "first_name": "Test",
                "last_name": "Buyer",
                "email": "buyer@example.com",
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        booking = Booking.objects.get()
        self.assertEqual(booking.total_amount, Decimal("250.00"))
        self.assertEqual(booking.get_total_cost(), Decimal("250.00"))
        self.assertEqual(booking.payment_status, Booking.PaymentStatus.PAID)
        self.assertEqual(response.data["total_amount"], "250.00")
        self.assertEqual(response.data["payment_status"], "paid")
        self.assertEqual(self.client.get("/api/cart/").data["items"], [])

    def test_paid_is_the_only_payment_status(self):
        self.assertEqual(list(Booking.PaymentStatus.values), ["paid"])
