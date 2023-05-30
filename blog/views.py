from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import (AllowAny, 
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Post, Comment, Like
from .permissions import IsAuthor
from .serializers import PostSerializer, CommentSerializer


"""листинг всех постов"""
class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


"""листинг поста по id"""
class PostRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


"""создание, обновление, удаление постов для авторизированных пользователей"""
class PostViewSet(mixins.CreateModelMixin, 
                  mixins.UpdateModelMixin, 
                  mixins.DestroyModelMixin, 
                  GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsAuthor]


"""создание, обновление, удаление комментариев к постам только от авторизированных пользователей"""
class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]


"""пользователь ставит лайки на посты """
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def toggle_like(request, p_id):
    post = get_object_or_404(Post, id=p_id)
    like = Like.objects.filter(user=request.user, post=post)
    if like.exists():
        like.delete()
        like = False
    else:
        Like.objects.create(user=request.user, post=post)
        like = True
    return Response({"Liked": like}, status=200)