from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST
from movies.models import Seat,Show
from .cart import Cart


# Create your views here.

@require_POST
def cart_add(request,seat_id, show_id):
    cart = Cart(request)
    seat = get_object_or_404(Seat,id = seat_id)
    show = get_object_or_404(Show,id =show_id)
    cart.add(seat=seat,show=show)

    return redirect('movies:seat_list', slug =show.slug)


@require_POST
def cart_remove(request,seat_id):
    cart = Cart(request)
    seat = get_object_or_404(Seat,id = seat_id)
    cart.remove(seat=seat)
    
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    show_id = cart.cart.get("show_id")
    if show_id is None:
        show = None
    else:
        id = int(show_id)
        show = get_object_or_404(Show,id = id)

    
    return render(request,'cart/detail.html',{
        'cart':cart,
        'show':show
        
    })