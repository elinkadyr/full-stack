from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryListCreateAPIView, CategoryDestroyAPIView

router = DefaultRouter()
router.register('product', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product/categories/', CategoryListCreateAPIView.as_view()),
    path('product/categories/<int:pk>/', CategoryDestroyAPIView.as_view()),
]