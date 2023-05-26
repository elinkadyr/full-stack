from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('post', PostViewSet, basename='post')
router.register('posts/comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/list/', PostListAPIView.as_view(), name='post-list'),
]
