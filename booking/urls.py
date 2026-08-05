from django.urls import path
from . import views
app_name = 'booking'

urlpatterns = [
    path('create/',views.booking_create,name = "booking_create"),
]
