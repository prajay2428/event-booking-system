from django.db import migrations, models
from django.utils.text import slugify


def populate_unique_slugs(apps, schema_editor):
    Movie = apps.get_model("movies", "Movie")
    used = set()

    for movie in Movie.objects.order_by("id"):
        base = slugify(movie.slug or movie.title)[:50] or "movie"
        candidate = base
        suffix = 2

        while candidate in used:
            suffix_text = f"-{suffix}"
            candidate = f"{base[:60 - len(suffix_text)]}{suffix_text}"
            suffix += 1

        if movie.slug != candidate:
            movie.slug = candidate
            movie.save(update_fields=["slug"])

        used.add(candidate)


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0006_alter_seat_price_delete_bookings"),
    ]

    operations = [
        migrations.RunPython(populate_unique_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="movie",
            name="slug",
            field=models.SlugField(blank=True, max_length=60, unique=True),
        ),
    ]
