from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('post', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('post/comment/', CommentAPIView.as_view()),
    path('post/comment/<int:id>', DeleteCommentAPIView.as_view()),
]
