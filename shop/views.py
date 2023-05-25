from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser


from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser]
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('size', 'color', 'gender', )
    search_fields = ('title', )


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDestroyAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

