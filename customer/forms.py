from django import forms
from . models import Address

class CreateAddress(forms.ModelForm):
    flat_no = forms.CharField(max_length=50, required=True)
    building = forms.CharField(max_length=100, required=True)
    area = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=100,)
    pin = forms.IntegerField()

    class Meta:
        model = Address
        fields = ['flat_no', 'building', 'area', 'city', 'pin']