from rest_framework import serializers

from blog.models import Post
from blog.serializers import PostSerializer

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
                  "avatar", 
                  "posts")
        

    def to_representation(self, instance):
        rep= super().to_representation(instance)
        posts = Post.objects.filter(user=instance.id)
        rep["posts"] = PostSerializer(posts, many=True).data
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

