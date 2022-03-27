from django import forms
from . models import Address, Payment, Review

numbers = ['0','1','2','3','4','5','6','7','8','9']

def check_number(value):
    for n in value:
        if n in numbers:
            raise  forms.ValidationError(value+" cannot contain numbers")
def check_pin(pin):
    pin_number = str(pin)
    if(len(pin_number)<6 or len(pin_number) >6):
        raise forms.ValidationError("Pin must be 6 digit only.")

def check_card(card):
    if(len(card)<16 or len(card)>16):
        raise forms.ValidationError("Enter valid 16 digit card number")

class CreateAddress(forms.ModelForm):
    flat_no = forms.CharField(max_length=50, required=True , error_messages={'required':'Please enter flat or room number.'})
    building = forms.CharField(validators=[check_number], max_length=100, required=True , error_messages={'required':'Please enter building name'})
    area = forms.CharField(validators=[check_number], max_length=100, required=True , error_messages={'required':'area is required'})
    city = forms.CharField(validators=[check_number], max_length=100, error_messages={'required':'Please enter city.'})
    pin = forms.IntegerField(validators=[check_pin] , error_messages={'required':'Pin is required'})

    class Meta:
        model = Address
        fields = ['flat_no', 'building', 'area', 'city', 'pin']

class PaymentForm(forms.ModelForm):
    card_number = forms.CharField(validators=[check_card],max_length=16, required=True, error_messages={'required':'Card number is required'})
    # building = forms.CharField(validators=[check_number], max_length=100, required=True)
    # area = forms.CharField(validators=[check_number], max_length=100, required=True)
    # city = forms.CharField(validators=[check_number], max_length=100,)
    # pin = forms.IntegerField(validators=[check_pin])

    class Meta:
        model = Payment
        fields = ['card_number']

class AddReview(forms.ModelForm):
    # id = models.AutoField(primary_key=True)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = forms.CharField(max_length=100, required=True, error_messages={'required':'Title is required'})
    description = forms.CharField(max_length=255, required=True, error_messages={'required':'Descritption is required'})
    stars = forms.IntegerField(required=True, error_messages={'required':'Please enter stars'})
    class Meta:
        model = Review
        fields = ['title', 'description', 'stars']