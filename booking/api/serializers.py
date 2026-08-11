# booking/api/serializers.py

from rest_framework import serializers
from booking.models import Booking, BookingSeat


class BookingSeatSerializer(serializers.ModelSerializer):
    seat_name = serializers.CharField(source="seat.name")

    class Meta:
        model = BookingSeat
        fields = [
            "seat_name",
            "price_paid",
        ]


class BookingSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source="show.movie.title")
    theatre = serializers.CharField(source="show.theatre")
    date = serializers.DateField(source="show.date")
    time = serializers.TimeField(source="show.time")

    bookingseat = BookingSeatSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "movie",
            "theatre",
            "date",
            "time",
            "amount_paid",
            "payment_status",
            "created",
            "bookingseat",
        ]


class BookingCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()