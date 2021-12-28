from django.db import models
from home.models import User

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
        return str(self.flat_no)



class Payment(models.Model):
    payments = (
        ('COD', 'COD'),
        ('UPI', 'UPI'),
        ('Net Banking', 'Net Banking'),

    )
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=100, choices=payments)
    card_number = models.CharField(max_length=100, blank=True, null=True)
    amount = models.IntegerField(default=5000)

    def __str__(self):
        return "Payment Type = " + self.payment_type
        

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.name
        
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    model = models.CharField(max_length=255, blank=False, null=False)
    short_description = models.CharField(max_length=255, blank=False, null=False)
    camera = models.CharField(max_length=255, blank=False, null=False)
    display = models.CharField(max_length=255, blank=False, null=False)
    memory = models.CharField(max_length=100, blank=False, null=False)
    processor = models.CharField(max_length=100, blank=False, null=False)
    os = models.CharField(max_length=100, blank=False, null=False)
    image = image = models.ImageField(upload_to='productimg')
    quantity = models.IntegerField(blank=True, null=True)
    selling_price = models.IntegerField(default=8000, blank=True)
    discount_price = models.IntegerField(default=8000)

    def __str__(self):
        return str(self.id)+" "+self.model


 

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    item = models.IntegerField(default=1)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

order_status = (
    ('Ordered', 'Ordered'),
    ('Pending', 'Pending'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=False, null=False)
    date = models.DateField()
    total_amount = models.IntegerField()
    status = models.CharField(max_length=100, choices=order_status, default='ordered')
    def __str__(self):
        return str(self.id)


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    stars = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title + ' '+ str(self.stars)
