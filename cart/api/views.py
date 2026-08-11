# cart/api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from movies.models import Seat,Show
from django.shortcuts import get_object_or_404

from cart.cart import Cart
from .serializers import CartItemSerializer


class CartDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        cart = Cart(request)

        serializer = CartItemSerializer(
            list(cart),
            many=True
        )

        return Response(
            {
                "items": serializer.data,
            },
            status=status.HTTP_200_OK
        )

class CartAddView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, seat_id, show_id):
        cart = Cart(request)
        show = get_object_or_404(Show,id = show_id)
        seat = get_object_or_404(Seat,id = seat_id)
        cart.add(seat=seat, show=show)

        return Response(
            {
                "message": "item added successfully",
            },
            status =status.HTTP_200_OK
        )

class CartRemoveView(APIView):
    permission_classes = [AllowAny]

    def post(self,request,seat_id):
        cart = Cart(request)
        seat = get_object_or_404(Seat,id = seat_id)
        cart.remove(seat=seat)

        return Response(
            {"message" : "item removed successfully",},
            status=status.HTTP_200_OK
        )
        