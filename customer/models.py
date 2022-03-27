from django.db import models
from home.models import User
import datetime

# Create your models here.

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flat_no = models.CharField(max_length=50, blank=True, null=True)
    building = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    pin = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return str(self.id)+" "+ self.user.first_name + " " + self.area +" " + str(self.pin)



class Payment(models.Model):
    payments = (
        ('COD', 'COD'),
        ('UPI', 'UPI'),
        ('Net Banking', 'Net Banking'),
        ('Credit/Debit Card', 'Credit/Debit Card'),
    )
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100, choices=payments)
    card_number = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField(default=5000)

    def __str__(self):
        return "Payment = " + self.user_id.email +" " +self.payment_type + " "+ str(self.amount)
        

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.name
        
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE, null=False)
    model = models.CharField(max_length=255, blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=False, null=True)
    camera = models.CharField(max_length=255, blank=True, null=True)
    display = models.CharField(max_length=255, blank=True, null=True)
    memory = models.CharField(max_length=100, blank=True, null=True)
    processor = models.CharField(max_length=100, blank=True, null=True)
    os = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='productimg', null=True)
    quantity = models.IntegerField(blank=True, null=True)
    selling_price = models.IntegerField(default=8000,blank=True, null=True)
    discount_price = models.IntegerField(default=8000, blank=True, null=True)

    def __str__(self):
        return str(self.id)+" "+self.model

 

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id) + " " + self.product.model + " " + str(self.quantity)

    @property
    def total_cost(self):
        self.quantity * self.product.discount_price

order_status = (
    ('Ordered', 'Ordered'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1, blank=False, null=False)
    date = models.DateTimeField(default=datetime.datetime.now)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=100, choices=order_status, default='ordered')

    class Meta:
        ordering = ['-date',]

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product_id.discount_price


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    stars = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title + ' '+ str(self.stars)
