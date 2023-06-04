from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

from .tasks import send_activation_code


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)  
        user.create_activation_code()
        send_activation_code.delay(user.email, user.activation_code)
        user.save(using=self._db)
        Billing.objects.create(user=user)
        return user

    def create_superuser(self, email, password, **kwargs):
        if not email:
            raise ValueError("Email is required")
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True
        kwargs["is_active"] = True
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password) 
        user.save(using=self._db)
        return user



class MyUser(AbstractUser):
    username = None  # юзернейм отключен
    email = models.EmailField(unique=True) # Поле для почты
    name = models.CharField(max_length=100)  # Поле для имени
    last_name = models.CharField(max_length=100) # Поле для фамилии
    phone = models.CharField(max_length=50, blank=True, null=True) # Поле для телефона
    bio = models.TextField(max_length=500, blank=True, null=True)  # Поле биографии
    date_of_birth = models.DateField(null=True)  # Поле даты рождения
    programming_language = models.CharField(max_length=50, choices=[('javascript', 'JavaScript'), 
                                                    ('python', 'Python')])  # Поле языка программирования
    group = models.CharField(max_length=50, choices=[('JS 31', 'JS 31'), ('PY 27', 'PY 27')])  # Поле группы
    status = models.CharField(max_length=50, choices=[('student', 'student'), ('mentor', 'mentor')], null=True)
    social_media_link = ArrayField(models.URLField(), null=True, blank=True)  # Массив ссылок на социальные сети
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.jpg') # Поле для аватарки
    is_active = models.BooleanField(default=False) # обязательная активация через почту
    activation_code = models.CharField(max_length=10, blank=True) # отправка активационного кода


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return f'{self.id}   ->   {self.email}'
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name', ]

    objects = UserManager()

    def create_activation_code(self):
        from django.utils.crypto import get_random_string
        code = get_random_string(length=10) 
        self.activation_code = code
        self.save()


"""модель для чего то"""
class Billing(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='billing')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def top_up(self, amount):
        """Пополнение счета, если транзакция прошла успешно, вернется True"""
        if amount > 0:
            self.amount += amount
            self.save()
            return True
        return False

    def withdraw(self, amount):
        """Снятие денег со счета, если транзакция прошла успешно, вернется True"""
        if self.amount >= amount:
            self.amount -= amount
            self.save()
            return True
        return False

    def __str__(self):
        return self.user.email