from django import forms
from .models import *
import datetime

DATE = datetime.date.today()

class DateInput(forms.DateInput):
    input_type = 'date'

class BoulderForm(forms.ModelForm):
    class Meta:
        model = Boulder
        fields = ['color', 'grade', 'area', 'setter', 'date']
        widgets = {
            'date':DateInput(),
        }


    def __init__(self, *args, **kwargs):
        super(BoulderForm, self).__init__(*args, **kwargs)
        self.fields['date'].initial = DATE

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['color', 'grade', 'area', 'setter']

class AddManyForm(forms.ModelForm):
    class Meta:
        model = Boulder
        exclude = ()
class ClimbForm(forms.ModelForm):
    class Meta:
        model = Climb
        fields = ['color', 'grade', 'area']
AddmanyFormset = forms.modelformset_factory(Boulder, form=BoulderForm)
