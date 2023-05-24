from rest_framework.serializers import ModelSerializer
from .models import Category, Product, ProductImage


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    
    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        rep["images"] = ProductImageSerializer(instance.images.all(), many=True, context=self.context).data
        return rep


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get("request")
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["image"] = self._get_image_url(instance)
        return rep