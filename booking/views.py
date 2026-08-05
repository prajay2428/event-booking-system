from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import BookingCreateForm
from .models import Booking,BookingSeat
from movies.models import Seat,Show
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.db import IntegrityError, transaction
# Create your views here.


@login_required
def booking_create(request):
    cart = Cart(request)
    user = request.user

    show_id = cart.cart.get("show_id")
    if not show_id:
        messages.warning(request, "you haven't selected any seats")
        return redirect("movies:movie_list")
    
    show = get_object_or_404(Show, id=show_id)
    if  len(cart) == 0:
        messages.warning(request, "you have no seats selected in your cart")
        return redirect("movies:seat_list", slug = show.slug)

    amount = Decimal("0.00")
    for item in cart:
        amount += item["price"]

    if request.method == "POST":
        booking_form = BookingCreateForm(request.POST)

        if booking_form.is_valid():
            try:
                with transaction.atomic():
                    booking = booking_form.save(commit=False)
                    booking.user = user
                    booking.show = show
                    booking.amount_paid = amount
                    booking.payment_status = Booking.PaymentStatus.PAID
                    booking.save()

                    for item in cart:
                        BookingSeat.objects.create(
                            booking=booking,
                            seat=item["seat"],
                            show=show,
                            price_paid=item["price"],
                        )

            except IntegrityError:
                messages.error(
                    request,
                    "One or more selected seats were already booked. "
                    "Please choose different seats.",
                )
                return redirect(
                    "movies:seat_list",
                    slug=show.slug,
                )

            cart.clear()

            return render(
                request,
                "booking/created.html",
                {
                    "booking": booking,
                },
            )

    else:
        booking_form = BookingCreateForm()

    return render(
        request,
        "booking/create.html",
        {
            "form": booking_form,
            "cart": cart,
        },
    )