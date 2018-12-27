from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# ---------------------------------------------------------------------------------------------------------------------

class SignUpForm(UserCreationForm):

    org_name = forms.CharField(max_length=100, help_text='Organization Name')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('org_name', 'avatar', 'first_name', 'last_name', 'email', 'password1', 'password2')

# ---------------------------------------------------------------------------------------------------------------------
