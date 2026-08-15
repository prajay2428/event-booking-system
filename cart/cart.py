from copy import deepcopy
from decimal import Decimal

from django.conf import settings

from movies.models import Seat


class Cart:
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if cart is None:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def add(self, seat, show):
        if seat.theatre_id != show.theatre_id:
            raise ValueError("This seat does not belong to the show's theatre.")

        # Import locally to avoid a module-level circular dependency.
        from booking.models import BookingSeat

        if BookingSeat.objects.filter(show=show, seat=seat).exists():
            raise ValueError("This seat has already been booked.")

        show_id = str(show.id)
        seat_id = str(seat.id)
        price = str(seat.price)

        if not self.cart:
            self.cart["show_id"] = show_id
            self.cart["seats"] = {
                seat_id: {"price": price}
            }

        elif self.cart["show_id"] == show_id:
            self.cart["seats"][seat_id] = {
                "price": price
            }

        else:
            self.cart.clear()
            self.cart["show_id"] = show_id
            self.cart["seats"] = {
                seat_id: {"price": price}
            }

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, seat):
        """Remove a seat from the cart."""
        seat_id = str(seat.id)
        seats = self.cart.get("seats", {})

        if seat_id in seats:
            del seats[seat_id]

        if not seats:
            self.cart.clear()

        self.save()

    def __iter__(self):
        cart_seats = self.cart.get("seats", {})
        seat_ids = cart_seats.keys()

        seats = Seat.objects.filter(id__in=seat_ids)

        # Prevent adding model objects to the actual session dictionary.
        cart = deepcopy(cart_seats)

        for seat in seats:
            cart[str(seat.id)]["seat"] = seat

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            yield item

    def get_total_cost(self):
        return sum(
            (
                Decimal(item["price"])
                for item in self.cart.get("seats", {}).values()
            ),
            Decimal("0.00"),
        )

    def __len__(self):
        return len(self.cart.get("seats", {}))

    def clear(self):
        self.session.pop(settings.CART_SESSION_ID, None)
        self.save()
