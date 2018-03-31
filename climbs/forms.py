from django import forms
from .models import *
import datetime

DATE = datetime.date.today()

class DateInput(forms.DateInput):
    input_type = 'date'

class ClimbCreateForm(forms.ModelForm):
    class Meta:
        model = Climb
        fields = ['color', 'grade', 'area', 'setter', 'date_created']
        widgets = {
            'date':DateInput(),
        }


    def __init__(self, *args, **kwargs):
        super(ClimbCreateForm, self).__init__(*args, **kwargs)
        self.fields['date_created'].initial = DATE

class AddManyForm(forms.ModelForm):
    class Meta:
        model = Climb
        exclude = ()

class ClimbForm(forms.ModelForm):
    class Meta:
        model = Climb
        fields = ['anchor', 'color', 'grade', 'area', 'setter']


AddmanyFormset = forms.modelformset_factory(Climb, form=ClimbCreateForm)
