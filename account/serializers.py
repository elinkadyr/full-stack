from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from blog.models import Post, Favorite
from blog.serializers import PostSerializer, FavoriteSerializer

from .models import MyUser

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
                  "status",
                  "phone", 
                  "date_of_birth", 
                  "programming_language", 
                  "group", 
                  "social_media_link", 
                  "avatar",)
        

    def to_representation(self, instance):
        rep= super().to_representation(instance)
        posts = Post.objects.filter(user=instance.id)
        rep["posts"] = PostSerializer(posts, many=True).data
        favorites = Favorite.objects.filter(user=instance.id)
        rep["in_favorites"] = FavoriteSerializer(favorites, many=True).data
        return rep

"""
Внутри метода to_representation() выполняются следующие действия:

    Вызывается метод to_representation() базового класса,
        чтобы получить представление экземпляра модели по умолчанию.

    Создается переменная posts, которая содержит все объекты модели Post, 
        связанные с указанным пользователем (user=instance.id).

    Создается новый ключ "posts" в словаре rep, 
        и в качестве значения устанавливается 
        сериализованное представление всех постов (PostSerializer(posts, many=True).data).

    Возвращается обновленное представление экземпляра модели rep.

Этот код добавляет сериализованное представление всех постов, 
связанных с указанным пользователем, в представление экземпляра модели. 
    Таким образом, при сериализации экземпляра модели, 
    возвращается словарь с данными экземпляра и дополнительным ключом "posts", 
    содержащим сериализованное представление всех постов пользователя. 
"""



"""сериализатор для отображения всех пользователей"""
class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 
                  'email', 
                  'avatar', 
                  'name', 
                  'last_name',
                  'programming_language',
                  'group',
                  'status')


"""когда забыл пароль"""
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=100)

    def validate(self, data):
        email = data.get("email")
        user = MyUser.objects.filter(email=email).last()
        if not user:
            raise serializers.ValidationError(
                "You don't have an account. Please create one."
            )
        return data

class CheckTokenSerializer(serializers.Serializer):
    uidb64_regex = r"[0-9A-Za-z_\-]+"
    token_regex = r"[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}"
    uidb64 = serializers.RegexField(uidb64_regex)
    token = serializers.RegexField(token_regex)
    error_message = {"__all__": ("Invalid password reset token")}

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = MyUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            user = None
        return user


"""когда восстанавливаешь пароль"""
class ResetPasswordSerializer(CheckTokenSerializer):
    new_password1 = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate(self, data):
        self.user = self.get_user(data.get("uid"))
        if not self.user:
            raise serializers.ValidationError(self.error_message)
        is_valid_token = default_token_generator.check_token(
            self.user, data.get("token")
        )
        if not is_valid_token:
            raise serializers.ValidationError(self.error_message)
        new_password2 = data.get("new_password2")
        new_password1 = data.get("new_password1")
        if new_password1 != new_password2:
            raise serializers.ValidationError("The two password fields didn't match.")
        return new_password2