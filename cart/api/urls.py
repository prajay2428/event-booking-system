# cart/api/urls.py

from django.urls import path
from . import views


app_name = "cart"

urlpatterns = [
    path("", views.CartDetailView.as_view(), name="cart_detail"),
    path("add/<int:seat_id>/<int:show_id>", views.CartAddView.as_view(), name = "cart_add"),
    path("remove/<int:seat_id>", views.CartRemoveView.as_view(), name="cart_remove")
]