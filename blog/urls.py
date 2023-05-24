from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('post', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('post-like/<int:id>', toggle_like),
    path('comment/create/', CreateCommentAPIView.as_view()),
    path('comment/update/<int:pk>/', UpdateCommentAPIView.as_view()),
    path('comment/delete/<int:pk>/', DeleteCommentAPIView.as_view()),
]
