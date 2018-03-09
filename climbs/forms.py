from django import forms
from .models import *

class DateInput(forms.DateInput):
    input_type = 'date'

class BoulderForm(forms.ModelForm):
    class Meta:
        model = Boulder
        fields = ['color', 'grade', 'area', 'setter']
        widgets = {
            'date':DateInput(),
        }

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['color', 'grade', 'area', 'setter']

class AddManyForm(forms.ModelForm):
    class Meta:
        model = Boulder
        exclude = ()

AddmanyFormset = forms.modelformset_factory(Boulder, form=BoulderForm)
