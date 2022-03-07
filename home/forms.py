
# inbuilt library to create form fields attributes
from django import forms
# To create form structure and restriction import this
from django.contrib.auth.forms import UserCreationForm

# stor user in this model
from home.models import User

symbols = ['~','`','!','@','#','$','%','^','&','*','(',')','-','+','=','{','}','[',']','|','/','\\',':',';','\"','\'','<','>',',','?']
numbers = ['0','1','2','3','4','5','6','7','8','9']

#For registration of user
def check_username(username):
    first_char = username[0]
    print(first_char)
    if first_char in numbers or first_char in symbols:
        raise forms.ValidationError("Invalid Username, username cannot start with number and special character")
    for val in username:
        if val in symbols:
            raise forms.ValidationError(f"Invalid Username, username cannot contain {val} and other special characters")
    # print(len(username))
    length = len(username)
    if length < 3 or length > 15:
        raise forms.ValidationError("Invalid Username, username length should be greater than 2 and less than 16")

def check_password(password):
    if not any(char in symbols for char in password):
        raise forms.ValidationError("Password should contain at least one special character.")

    if not any(num in numbers for num in password):
        raise forms.ValidationError("Password should contain at least one number")

def check_contact(contact):
    if(len(contact) < 10):
        raise forms.ValidationError("Contact must be a 10 digit number")

def check_name(name):
    for num in numbers:
        if num in name:
            raise forms.ValidationError("Enter valid name")

    
class UserCreate(UserCreationForm, forms.ModelForm, forms.Form):
    # Giving restriction to the some form attributes
    user_name = forms.CharField(validators=[check_username], error_messages={'required':'Username is required'}, required=True)
    first_name = forms.CharField(validators=[check_name],
        max_length=30, help_text='Optional.')
    last_name = forms.CharField(validators=[check_name],
        max_length=30,  help_text='Optional.')  # necessary if required=True
    password1 = forms.CharField(validators=[check_password],error_messages={'required':'Password is required','min_length':'Password length must be greater than 8 character.',},
        min_length=8, max_length=15, required=True)  
    password2 = forms.CharField(validators=[check_password],error_messages={'required':'Please confirm your password',},
        min_length=8, max_length=15, required=True)  
    email = forms.EmailField(error_messages={'required':'Email is required'},
        max_length=254)
    contact = forms.CharField(validators=[check_contact],error_messages={'required':'Contact is required', 'max_length':'Contact must be 10 digit number'},
        max_length=10)

    # structure
    class Meta:
        # Store these data in this model
        model = User

        # Take these values from user and check
        fields = ('user_name', 'password1', 'password2',
                  'first_name', 'last_name', 'email', 'contact')

   
   
