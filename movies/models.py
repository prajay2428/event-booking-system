from django.db import models
from django.utils.text import slugify
from django.conf import settings
# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank = True, max_length=60)
    poster = models.ImageField(upload_to='posters/%Y/%m/%d/', blank=True)
    description = models.TextField(blank = True)
    director = models.CharField(max_length = 50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    release_date = models.DateTimeField()

    class Meta:
        indexes = [models.Index(fields=["slug"])]
        ordering = ["release_date"]

    def __str__(self):
        return self.title

class Theatre(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.name




class Seat(models.Model):
    theatre = models.ForeignKey(Theatre,on_delete=models.CASCADE,related_name="seats")
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=4,decimal_places=2)

    class Category(models.TextChoices):
        PREMIUM = "PREMIUM", "Premium"
        GOLD = "GOLD", "Gold"
        SILVER = "SILVER", "Silver"

    category = models.CharField(
        max_length=10,
        choices=Category.choices
    )
    def __str__(self):
        return self.name



class Show(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="show")
    theatre = models.ForeignKey(Theatre,on_delete=models.CASCADE,related_name="show")
    date = models.DateField()
    time = models.TimeField()
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
    )


    class Meta:
        ordering = ["date"]
        indexes = [models.Index(fields=["date","time"])]
        constraints = [
        models.UniqueConstraint(
            fields=["movie", "theatre", "date", "time"],
            name="unique_show"
        )
    ]
    def save(self, *args, **kwargs):

        self.slug = slugify(
            f"{self.movie.title}-{self.theatre.name}-{self.date}-{self.time}"
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.time} {self.date}"

class Bookings(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="bookings")
    theatre = models.ForeignKey(Theatre,on_delete=models.CASCADE,related_name="bookings")
    show = models.ForeignKey(Show,on_delete=models.CASCADE,related_name="bookings")
    seat = models.ForeignKey(Seat,on_delete=models.CASCADE,related_name="bookings")
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="bookings")

    def __str__(self):

        return f"{self.show.movie.title} - {self.seat.name}"