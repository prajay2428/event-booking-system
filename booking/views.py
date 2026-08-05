from django.shortcuts import render, get_object_or_404
from .forms import BookingCreateForm
from .models import Booking,BookingSeat
from movies.models import Seat,Show
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from decimal import Decimal
# Create your views here.


@login_required
def booking_create(request):
    cart = Cart(request)
    user = request.user
    show_id = int(cart.cart.get("show_id"))
    show = get_object_or_404(Show,id = show_id)
    amount = Decimal("0.00")
    for item in cart:
        amount += item["price"]


    if request.method =='POST':
        booking_form = BookingCreateForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = user
            booking.show = show
            booking.amount_paid = amount 
            booking.payment_status = Booking.PaymentStatus.PAID
            booking.save()
            for item in cart:
                booking_seat = BookingSeat()
                booking_seat.booking = booking
                booking_seat.seat = item["seat"]
                booking_seat.price_paid = item["price"]
                booking_seat.save()

            cart.clear()

            return render(request,'booking/created.html', {
                "booking_form" : booking_form,
                "cart" : cart,
                "booking" : booking,
                
            })

    else:
        booking_form = BookingCreateForm()
        return render(request,'booking/create.html', {
            "booking" : booking,
            "form":booking_form,
            "cart" : cart
            
        })

