from rest_framework import serializers
from movies.models import Movie, Show, Seat
from cart.cart import Cart
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['title','slug','poster','description','director','release_date']


class ShowSerializer(serializers.ModelSerializer):
    movie = serializers.StringRelatedField()
    theatre = serializers.StringRelatedField()
    class Meta:
        model = Show
        fields = ['movie','theatre','date','time','slug']


class SeatSerializer(serializers.ModelSerializer):
    theatre = serializers.StringRelatedField()
    isBooked = serializers.SerializerMethodField()
    isInCart = serializers.SerializerMethodField()
    showId = serializers.SerializerMethodField()
    movie = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    def get_showId(self, obj):
        return self.context["show"].id

    def get_movie(self, obj):
        return self.context["show"].movie.title

    def get_date(self, obj):
        return self.context["show"].date

    def get_time(self, obj):
        return self.context["show"].time
    def get_isBooked(self,obj):
        booked_seats = self.context["booked_seats"]
        if obj.id in booked_seats:
            return True
        else:
            return False

    def get_isInCart(self,obj):
        cart = Cart(self.context["request"])
        seats_in_cart = []
        for item in cart:
            seats_in_cart.append(item["seat"])

        return obj in seats_in_cart


    class Meta:
        model = Seat
        fields = [
            'id', 'showId', 'movie', 'theatre', 'date', 'time', 'name',
            'price', 'category', 'isBooked', 'isInCart'
        ]
