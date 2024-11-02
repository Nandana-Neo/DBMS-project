from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .validators import validate_nitc_email,validate

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_nitc_email]) # default is when required is true -- adds this field also to the form
    class Meta:
        model = User
        fields = ['first_name','username', 'email','password1','password2'] # field names of the user table

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = 'Student'

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(validators=[validate_nitc_email]) 
    class Meta:
        model = User
        fields = [ 'email', 'first_name']

class ProfileUpdateImgForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
class ProfileUpdateAboutForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about']