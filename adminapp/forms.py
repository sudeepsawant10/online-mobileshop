from django import forms
from customer.models import Product, Brand

class AddProduct(forms.ModelForm, forms.Form):
    model = forms.CharField(max_length=255, required=True, error_messages={'required':'Please enter model name',})
    short_description = forms.CharField(max_length=255, required=True, error_messages={'required':'Please enter short_description for model',})
    camera = forms.CharField(max_length=255, required=True, error_messages={'required':'Please enter camera details',})
    display = forms.CharField(max_length=255, required=True, error_messages={'required':'Please enter display details',})
    memory = forms.CharField(max_length=100, required=True, error_messages={'required':'Please enter memroy details',})
    processor = forms.CharField(max_length=100, required=True, error_messages={'required':'Processor details are required',})
    os = forms.CharField(max_length=100, required=True, error_messages={'required':'Model os is required',})
    image = forms.ImageField(required=True, error_messages={'required':'Image of model is required',})
    quantity = forms.IntegerField(required=True, error_messages={'required':'Please enter quantity available.',})
    selling_price = forms.IntegerField(required=True, error_messages={'required':'Selling_price is required',})
    discount_price = forms.IntegerField(required=True, error_messages={'required':'Discount_price is required',})

    class Meta:
        model = Product
        fields = ['model','short_description','camera','display','memory','processor','os','image','quantity','selling_price','discount_price']
        # fields = ['model','short_description','camera','image']

