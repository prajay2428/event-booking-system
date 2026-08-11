# booking/api/views.py

from decimal import Decimal

from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from booking.models import Booking, BookingSeat
from movies.models import Show
from cart.cart import Cart

from .serializers import (
    BookingSerializer,
    BookingCreateSerializer,
)

class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            user=self.request.user
        )

class BookingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = Cart(request)

        show_id = cart.cart.get("show_id")

        if not show_id:
            return Response(
                {
                    "message": "You haven't selected any seats."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(cart) == 0:
            return Response(
                {
                    "message": "Your cart is empty."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        show = get_object_or_404(
            Show,
            id=show_id
        )

        serializer = BookingCreateSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = Decimal("0.00")

        for item in cart:
            amount += item["price"]

        try:
            with transaction.atomic():

                booking = Booking.objects.create(
                    user=request.user,
                    first_name=serializer.validated_data["first_name"],
                    last_name=serializer.validated_data["last_name"],
                    email=serializer.validated_data["email"],
                    show=show,
                    amount_paid=amount,
                    payment_status=Booking.PaymentStatus.PAID,
                )

                for item in cart:
                    BookingSeat.objects.create(
                        booking=booking,
                        seat=item["seat"],
                        show=show,
                        price_paid=item["price"],
                    )

        except IntegrityError:
            return Response(
                {
                    "message":
                    "One or more selected seats were already booked."
                },
                status=status.HTTP_409_CONFLICT
            )

        cart.clear()

        output_serializer = BookingSerializer(
            booking
        )

        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED
        )