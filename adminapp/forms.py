from django import forms
from customer.models import Product, Brand

class AddProduct(forms.ModelForm):
    model = forms.CharField(max_length=255, required=True)
    short_description = forms.CharField(max_length=255, required=True)
    camera = forms.CharField(max_length=255, required=True)
    display = forms.CharField(max_length=255, required=True)
    memory = forms.CharField(max_length=100, required=True)
    processor = forms.CharField(max_length=100, required=True)
    os = forms.CharField(max_length=100, required=True)
    image = forms.ImageField(required=True)
    quantity = forms.IntegerField(required=True)
    selling_price = forms.IntegerField(required=True)
    discount_price = forms.IntegerField(required=True)

    class Meta:
        model = Product
        fields = ['model','short_description','camera','display','memory','processor','os','image','quantity','selling_price','discount_price']
        # fields = ['model','short_description','camera','image']

"""
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
"""