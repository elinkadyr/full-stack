from django.contrib import admin
from .models import MyUser, Billing

admin.site.register(MyUser)
admin.site.register(Billing)