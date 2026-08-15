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
        show = None
        show_id = cart.cart.get("show_id")

        if show_id:
            show = Show.objects.filter(id=show_id).select_related(
                "movie", "theatre"
            ).first()

        serializer = CartItemSerializer(
            list(cart),
            many=True
        )
        return Response(
            {
                "items": serializer.data,
                "show": {
                    "id": show.id,
                    "slug": show.slug,
                    "movie": show.movie.title,
                    "theatre": show.theatre.name,
                    "date": show.date,
                    "time": show.time,
                } if show else None,
                "total": cart.get_total_cost(),
            },
            status=status.HTTP_200_OK
        )

class CartAddView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, seat_id, show_id):
        cart = Cart(request)
        show = get_object_or_404(Show,id = show_id)
        seat = get_object_or_404(Seat,id = seat_id)
        try:
            cart.add(seat=seat, show=show)
        except ValueError as error:
            return Response(
                {"message": str(error)},
                status=status.HTTP_409_CONFLICT,
            )

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
