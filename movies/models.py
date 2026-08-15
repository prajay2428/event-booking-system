from django.db import models
from django.utils.text import slugify
from django.conf import settings
# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, max_length=60, unique=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:50] or "movie"
            slug = base_slug
            suffix = 2

            while Movie.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                suffix_text = f"-{suffix}"
                slug = f"{base_slug[:60 - len(suffix_text)]}{suffix_text}"
                suffix += 1

            self.slug = slug

        super().save(*args, **kwargs)

class Theatre(models.Model):
    name = models.CharField(max_length = 100)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.name




class Seat(models.Model):
    theatre = models.ForeignKey(Theatre,on_delete=models.CASCADE,related_name="seats")
    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=6,decimal_places=2)

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
        return f"{self.movie.title} {self.time} {self.date}"

