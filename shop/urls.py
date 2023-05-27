from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CategoryListCreateAPIView, 
                    CategoryDestroyAPIView, 
                    ProductListAPIView,
                    ProductRetrieveAPIView,
                    ProductCreateAPIView,
                    ProductUpdateDestroyAPIView,
                    CommentViewSet, 
                    AddRatingAPIView)


router = DefaultRouter()
router.register("products/comments", CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/categories/', CategoryListCreateAPIView.as_view()),
    path('products/categories/<int:pk>/', CategoryDestroyAPIView.as_view()),   
    path('products/listing/', ProductListAPIView.as_view(), name='product-list'),
    path('products/listing/<int:pk>/', ProductRetrieveAPIView.as_view(), name='product-retrieve'),
    path('products/', ProductCreateAPIView.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductUpdateDestroyAPIView.as_view(), name='product-update-destroy'),
    path('products/add_rating/', AddRatingAPIView.as_view()),
]
