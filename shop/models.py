from django.db import models
from statistics import mean

from account.models import MyUser

"""модель для категории"""
class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.id}   ->  {self.title}'

'''модель для продуктов'''
class Product(models.Model):
    SIZE_CHOICES = [
        ('s', 'small'),
        ('m', 'medium'),
        ('l', 'large'),
    ]

    COLOR_CHOICES = [
        ('red', 'red'),
        ('blue', 'blue'),
        ('green', 'green'),
        ('yellow', 'yellow'),
        ('brown', 'brown'),
        ('black', 'black'),
        ('white', 'white'),
        ('gray', 'gray'),
    ]

    GENDER_CHOICES = [
        ('male', 'male'),
        ('female', 'female'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products') # категория
    title = models.CharField(max_length=100) # название продукта
    description = models.TextField(blank=True) # описание дродукта
    price = models.DecimalField(max_digits=10, decimal_places=2)  # цена продукта
    size = models.CharField(max_length=50, choices=SIZE_CHOICES) # размер
    color = models.CharField(max_length=50, choices=COLOR_CHOICES) # цвет
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES) # гендер
    quantity = models.IntegerField() # количество товара 
    image1 = models.ImageField(upload_to='shop/', null=True, blank=True) # фоточка 1
    image2 = models.ImageField(upload_to='shop/', null=True, blank=True) # фоточка 2
    
    def __str__(self):
        return f'{self.id} -> {self.title}'

    @property
    def get_average_rating(self):
        ratings = self.ratings.all().values_list('value', flat=True)
        if ratings:
            return mean(ratings)
        return 0


"""модель для комментариев"""
class Comment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='product_comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'<{self.product.title}> commented by <{self.user.email}>'


"""модель рейтинга для продуктов"""
class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4), (5,5)])

    def __str__(self):
        return f"<{self.product}> rated by <{self.user.email}>"
    

"""модель для избранного для продуктов"""
class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'<{self.product.title}> added to favorites by {self.user.email}'