from rest_framework.serializers import ModelSerializer

from .models import Post, Comment



class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.all().count()
        comments = instance.comments.all()
        rep['comments'] = CommentSerializer(comments, many=True).data
        return rep


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['user']
    
    def validate(self, attrs):
        super().validate(attrs)
        request = self.context.get("request")
        attrs['user'] = request.user
        return attrs