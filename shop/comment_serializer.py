from rest_framework import serializers

from .models import Comment


"""сериализатор для комментариев к продуктам"""
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['user']
        ref_name = 'shop_comment'
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('request').user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep  = super().to_representation(instance)
        rep['user'] = instance.user.email
        rep['name'] = instance.user.name
        rep['avatar'] = instance.user.avatar.url   
        return rep
