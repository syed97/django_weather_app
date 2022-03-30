from django import forms
from .models import City

class AddCityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name' : forms.TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'})}


# class DeleteCityForm(forms.ModelForm):
#     # multiple choice option
#     cities = forms.MultipleChoiceField(
#         choices = tuple([(obj.id, obj.name) for obj in City.objects.all()])
#     )    

#     class Meta:
#         model = City
#         fields = ['cities']

#     # def __init__(self, *args, **kwargs):
#     #     super(DeleteCityForm, self).__init__(*args, **kwargs)
#     #     self.fields['cities'].required = False

        