from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


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

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50, choices=COLOR_CHOICES)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    quantity = models.IntegerField()
    image1 = models.ImageField(upload_to='shop/', null=True, blank=True)
    image2 = models.ImageField(upload_to='shop/', null=True, blank=True)
    
    def __str__(self):
        return self.title
