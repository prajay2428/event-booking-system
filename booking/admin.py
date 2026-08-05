from django.contrib import admin
from .models import Booking,BookingSeat
# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display=['user','email','show','amount_paid','payment_status','created']

@admin.register(BookingSeat)
class BookingSeatAdmin(admin.ModelAdmin):
    list_display=['booking','seat','show','price_paid']