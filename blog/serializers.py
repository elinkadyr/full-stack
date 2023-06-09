from rest_framework import serializers

from .models import Post, Comment, Like, Favorite


"""сериализатор для постов"""
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 
                  'title',
                  'body', 
                  'image', 
                  'created_at',
                  'user',)
                  
    def to_representation(self, instance:Post):
        rep = super().to_representation(instance)
        rep['name'] = instance.user.name
        rep['last_name'] = instance.user.last_name
        rep['avatar'] = instance.user.avatar.url      
        comments = Comment.objects.filter(post=instance)
        rep["post_comments"] = CommentSerializer(comments, many=True).data
        rep["likes"] = instance.likes.all().count()
        rep["liked_by_user"] = False
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            rep["liked_by_user"] = Like.objects.filter(user=request.user, post=instance).exists()
        return rep


"""сериализатор для комментариев для постов"""
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('user',)
        ref_name = 'blog_comment'

    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep  = super().to_representation(instance)
        rep['user'] = instance.user.email
        rep['name'] = instance.user.name
        rep['avatar'] = instance.user.avatar.url      
        return rep


"""сериализатор для избранного для постов"""
class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Favorite
        fields = ('user', 'post')   