from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (PostListAPIView, 
                    PostRetrieveAPIView,
                    PostViewSet,   
                    CommentViewSet, 
                    toggle_like,
                    PostAddFavoriteAPIView)


router = DefaultRouter()
router.register('post', PostViewSet)
router.register('posts/comment', CommentViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('posts/list/', PostListAPIView.as_view(), name='posts-list'),
    path('posts/list/<int:pk>/', PostRetrieveAPIView.as_view(), name='post-list'),
    path('post/toggle_like/<int:p_id>/', toggle_like, name='post-like'),
    path('post/add_favorite/<int:pk>/', PostAddFavoriteAPIView.as_view()),
]
