from rest_framework import serializers  
from drf_yasg.utils import swagger_serializer_method
from .models import MyUser

from blog.serializers import PostSerializer
from blog.models import Post


"""сериализатор для регистрации пользователя"""
class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta:
        model = MyUser
        fields = ('name', 'last_name', 'email', 'password', 'password_confirm', )

    def validate(self, attrs):
        pass1 = attrs.get("password")
        pass2 = attrs.pop("password_confirm")
        if pass1 != pass2:
            raise serializers.ValidationError("passwords do not match")
        return attrs
    
    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('user with this email already exists')
        return email
    
    def create(self, validated_data):
        return MyUser.objects.create_user(**validated_data)


"""сериализатор для отображения профиля пользователя"""                 
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ("id", 
                  "email", 
                  "name", 
                  "last_name", 
                  "bio", 
                  "phone", 
                  "date_of_birth", 
                  "programming_language", 
                  "group", 
                  "social_media_link", 
                  "avatar", 
                  "posts")
        
    def to_representation(self, instance):
        rep= super().to_representation(instance)
        posts = Post.objects.filter(user=instance.id)
        rep["posts"] = PostSerializer(posts, many=True).data
        return rep


"""сериализатор для отображения всех пользователей"""
class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 
                  'email', 
                  'avatar', 
                  'name', 
                  'last_name')

