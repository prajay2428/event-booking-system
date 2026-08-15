from django.test import TestCase
from django.utils import timezone

from .models import Movie


class MovieModelTests(TestCase):
    def test_slug_is_generated_and_made_unique(self):
        first = Movie.objects.create(
            title="Same Movie",
            director="Director",
            release_date=timezone.now(),
        )
        second = Movie.objects.create(
            title="Same Movie",
            director="Director",
            release_date=timezone.now(),
        )

        self.assertEqual(first.slug, "same-movie")
        self.assertEqual(second.slug, "same-movie-2")
