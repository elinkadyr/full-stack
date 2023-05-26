from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


"""листинг товаров и создание нового товара"""
class ProductListCreateView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('size', 'color', 'gender', )
    search_fields = ('title', )


"""get запрос на один товар, обновление и удаление товара"""
class ProductRetrieveUpdateDestroyView(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser]


"""создание и просмотр категорий"""
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


"""удаление категории"""
class CategoryDestroyAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

