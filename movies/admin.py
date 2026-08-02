from django.contrib import admin
from .models import Movie,Show,Bookings,Theatre,Seat
# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display=['title','slug','director','release_date']
    prepopulated_fields={'slug' : ('title',)}


@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display=['name','address']

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display=['movie','theatre','date','time','slug']


@admin.register(Bookings)
class BookingAdmin(admin.ModelAdmin):
    list_display=['movie','theatre','show','seat','booked_by']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display=['theatre','name','price','category']