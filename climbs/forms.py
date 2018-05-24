from django import forms
from .models import *
import datetime
from django.forms import modelformset_factory
DATE = datetime.date.today()

class DateInput(forms.DateInput):
    input_type = 'date'

class ClimbCreateForm(forms.ModelForm):
    class Meta:
        model = Climb
        fields = ['color', 'grade', 'area', 'setter', 'date_created']
        widgets = {
            'date_created':DateInput(),
        }


    def __init__(self, *args, **kwargs):
        gym = kwargs.pop('gym')
        super(ClimbCreateForm, self).__init__(*args, **kwargs)
        self.fields['date_created'].initial = DATE
        self.fields['area'].queryset = Area.objects.filter(gym=gym)

class AddManyForm(forms.ModelForm):
    class Meta:
        model = Climb
        exclude = ()

class ClimbSelectForm(forms.ModelForm):
    class Meta:
        model = Climb
        fields = ['anchor','color',]

class ForemanClimbSelectForm(forms.ModelForm):
    class Meta:
        model = Climb
        fields = ['anchor', 'color', 'setter']

class ForemanClimbUpdateForm(forms.ModelForm):
    class Meta:
        model = Climb
        fields = ['anchor', 'color', 'grade', 'area', 'setter', 'date_created']
        widgets = {
            'date_created':DateInput(),
        }

    def __init__(self, *args, **kwargs):
        gym = kwargs.pop('gym')
        super(ForemanClimbUpdateForm, self).__init__(*args, **kwargs)
        self.fields['date_created'].initial = DATE
        self.fields['area'].queryset = Area.objects.filter(gym=gym)


class ClimbQueueModifyForm(forms.ModelForm):
    class Meta:
        model=Climb
        fields = ['grade', 'area']

    def __init__(self, *args, **kwargs):
        self.gym = kwargs.pop('gym')
        super(ClimbQueueModifyForm, self).__init__(*args, **kwargs)
        self.fields['area'].queryset = Area.objects.filter(gym=self.gym)

AddmanyFormset = forms.modelformset_factory(Climb, form=ClimbCreateForm)


BaseQueueFormset = modelformset_factory(Climb, form = ClimbQueueModifyForm, extra=0)
class QueueFormSet(BaseQueueFormset):

    def __init__(self, *args, **kwargs):
        #  create a user attribute and take it out from kwargs
        # so it doesn't messes up with the other formset kwargs
        self.gym = kwargs.pop('gym')
        super(QueueFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False

    def _construct_form(self, *args, **kwargs):
        # inject user in each form on the formset
        kwargs['gym'] = self.gym
        return super(QueueFormSet, self)._construct_form(*args, **kwargs)
