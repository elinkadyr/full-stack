from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.generics import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                         IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Category, Product, Comment, Rating, Favorite
from .permissions import IsAuthor
from .serializers import (CategorySerializer, 
                          ProductSerializer,
                          RatingSerializer)
from .comment_serializer import CommentSerializer


"""листинг всех товаров"""
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_fields = ('size', 'color', 'gender', )
    search_fields = ('title', 'description', )


"""листинг товара по id"""
class ProductRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


"""создание товара"""
class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser]


"""обновление и удаление товара по id"""
class ProductUpdateDestroyAPIView(generics.UpdateAPIView,
                                  generics.DestroyAPIView):
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


"""crud для комментариев"""
class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


"""рейтинг для продуктов"""
class AddRatingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RatingSerializer())
    def post(self, request):
        serializer = RatingSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        product = serializer.validated_data["product"]
        rating_value = serializer.validated_data["value"]

        try:
            rating_instance = Rating.objects.get(user=user, product=product)
            if rating_instance.value != rating_value:
                message = "Рейтинг изменен"
            else:
                message = "Рейтинг уже существует"
        except Rating.DoesNotExist:
            message = "Рейтинг создан"

        serializer.save(user=user)

        return Response({"message": message}, status=201)

    

"""добавлять продукты в избранное"""
class AddFavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        favor = Favorite.objects.filter(user=request.user, product=product)
        if favor.exists():
            favor.delete()
            favor = False
        else:
            Favorite.objects.create(user=request.user, product=product)
            favor = True
        return Response({'In Favorite': favor}, status=200)