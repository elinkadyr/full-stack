from django.urls import path

from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView, CategoryListCreateAPIView, CategoryDestroyAPIView

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-retrieve-update-destroy'),
    path('products/categories/', CategoryListCreateAPIView.as_view()),
    path('products/categories/<int:pk>/', CategoryDestroyAPIView.as_view()),
]
