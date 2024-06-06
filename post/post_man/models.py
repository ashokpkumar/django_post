from django.db import models
from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserModel(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    token = models.CharField(max_length=255,null=True, blank=True)
    token_created_date = models.DateTimeField(null=True, blank=True)

    def check_password(self, password):
        return password == self.password
    
class OrderModel(models.Model):
    order_id = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    priority = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    door_number = models.CharField(max_length=20)
    order_weight = models.DecimalField(max_digits=5, decimal_places=2)
    order_status = models.CharField(max_length=100, choices=[
        ('delivered', 'Delivered'),
        ('damaged', 'Damaged'),
        ('customer_not_reachable', 'Customer Not Reachable'),
        ('customer_rejects', 'Customer Rejects')
    ])