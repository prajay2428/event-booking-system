from django.db import models
from movies.models import Show,Seat
from django.conf import settings
from decimal import Decimal
# Create your models here.
class Booking(models.Model):
    class PaymentStatus(models.TextChoices):
        PROCESSING = "processing", "Processing"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='booking')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField()
    show = models.ForeignKey(Show,on_delete=models.CASCADE,related_name="bookings")
    amount_paid = models.DecimalField(max_digits=6,decimal_places=2)
    created = models.DateTimeField(auto_now_add= True)
    payment_status = models.CharField(
        max_length=30,
        choices=PaymentStatus.choices,
    )

    def get_total_cost(self):
        return (sum (booking_seat.price_paid for booking_seat in self.bookingseat.all()), Decimal("0.00"))


    


    def __str__(self):

        return f"{self.show.movie.title} - {self.id}"


class BookingSeat(models.Model):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name='bookingseat')
    seat = models.ForeignKey(Seat,on_delete=models.CASCADE,related_name='bookingseat')
    show = models.ForeignKey(Show,on_delete=models.CASCADE,related_name='bookingseat')
    price_paid = models.DecimalField(max_digits=6,decimal_places=2)
    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["show","seat"],
            name ='unique_show_seat'
        )]

    def __str__(self):
        return f"{self.seat.name} - {self.show}"