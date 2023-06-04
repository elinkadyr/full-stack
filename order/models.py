from django.db import models


from account.models import MyUser
from shop.models import Product


"""модель Order предоставляет структуру для хранения информации о заказах пользователей, 
а свойство total_price позволяет вычислять общую стоимость каждого заказа на основе его элементов"""

class Order(models.Model):
	user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='orders')
	is_paid = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	
	@property
	def total_price(self):
		items = self.items.all()
		if items.exists():
			return sum([item.product.price * item.quantity for item in items])
		return 0
	

class OrderItem(models.Model):
	order = models.ForeignKey(
		Order,
		on_delete=models.CASCADE,
		related_name='items'
	)
	product = models.ForeignKey(
		Product,
		on_delete=models.RESTRICT
	)
	quantity = models.PositiveIntegerField(default=1)
	

