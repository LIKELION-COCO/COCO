from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserSignupForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username']

class CustomUserSigninForm(AuthenticationForm):
    class Meta(AuthenticationForm):
        model = CustomUser
        fields = ['username']