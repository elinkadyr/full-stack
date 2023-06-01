from rest_framework import serializers

from .models import Category, Product, Rating, Favorite
from .comment_serializer import CommentSerializer

"""сериализатор для комментариев в отдельном файле .comment_serializer.py"""

"""сериализатор для категорий продуктов"""
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


"""сериализатор для продуктов"""
class ProductSerializer(serializers.ModelSerializer):
    product_comments = CommentSerializer(many=True, read_only=True)
    ratings = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 
                  'category', 
                  'title', 
                  'description', 
                  'price', 
                  'size', 
                  'color', 
                  'gender', 
                  'quantity', 
                  'image1', 
                  'image2', 
                  'product_comments', 
                  'ratings', 
                  'user_rating')

    def get_ratings(self, instance):
        return instance.get_average_rating

    def get_user_rating(self, instance):
        request = self.context.get("request")
        if request.user.is_authenticated:
            try:
                rating = Rating.objects.get(user=request.user, product=instance)
                return rating.value
            except Rating.DoesNotExist:
                pass
        return 0


"""сериализатор длля рейтинга"""
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ("user",)

    def validate(self, attrs):
        super().validate(attrs)
        attrs["user"] = self.context["request"].user
        return attrs

    def create(self, validated_data):
        value = validated_data.pop("value")
        obj, created = Rating.objects.update_or_create(**validated_data, defaults={"value": value})
        return obj


"""сериализатор для избранного"""
class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Favorite
        fields = ('user', 'product')   
