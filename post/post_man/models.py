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
    
class Order(models.Model):
    order_id = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=100)
    door_number = models.CharField(max_length=20)
    apartment_number = models.CharField(max_length=20)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    ring_bell = models.BooleanField()
    google_link = models.CharField(max_length=255)
    landmark = models.CharField(max_length=100)
    
    order_weight = models.DecimalField(max_digits=5, decimal_places=2)
    item_type = models.CharField(max_length=100)
    battery_included = models.BooleanField()
    expected_delivery_date = models.DateField()
    priority = models.CharField(max_length=100,choices=[
        ('two_hours', 'two_hours'),
        ('one_day', 'one_day'),
        ('super_fast', 'super_fast'),
        ('normal', 'normal')
    ])

    order_status = models.CharField(max_length=100, choices=[
        ('delivered', 'Delivered'),
        ('damaged', 'Damaged'),
        ('customer_not_reachable', 'Customer Not Reachable'),
        ('customer_rejects', 'Customer Rejects'),
        ('available', 'Available')
    ])