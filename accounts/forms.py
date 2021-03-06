from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from climbs.models import Gym, Setter
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    # first_name = forms.CharField(max_length=20, required=True)
    # last_name = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')

class GymSelectionForm(forms.ModelForm):
    class Meta:
        model = Setter
        fields = ['current_gym']
