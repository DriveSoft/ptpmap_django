from django import forms
from .models import *
from django.core.exceptions import ValidationError


class PTPForm(forms.ModelForm):
    record_id = forms.IntegerField(required=False) #заносим сюда id записи, для редактирования
    datetime = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = ptp
        fields = ['city', 'latitude', 'longitude', 'description', 'datetime', 'ptptype', 'carRedSignal', 'carTurnLeft', 'carTurnRight', 'pedRedSignal', 'pedWrongCross', 'pedKid', 'danger', 'id']

        labels = {
            "city": "Град"
        }

        widgets = {
            'city': forms.Select(attrs={'class': 'form-control', 'id': 'city'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id': 'longitude'}),
            'description': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'id': 'description'}),
            'datetime': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'datetime'}),
            'ptptype': forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'ptptype'}),
            'carRedSignal': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'carRedSignal'}),
            'carTurnLeft': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'carTurnLeft'}),
            'carTurnRight': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'carTurnRight'}),
            'pedRedSignal': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'pedRedSignal'}),
            'pedWrongCross': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'pedWrongCross'}),
            'pedKid': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'pedKid'}),
            'danger': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'danger'}),
        }


"""
        widgets = {
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
        }
"""

"""
    def clean_lastname(self): # проверка данных
        if self.cleaned_data['lastname']:
            new_lastname = self.cleaned_data['lastname'].title() # приводим введенный слаш в нижний регистр

            if new_lastname == 'Create': # слово create запрещено для использования
                raise ValidationError('Lastname may not be "Create"')

            #if Person.objects.filter(lastname__iexact=new_lastname).count(): # проверяем уникальность введеного слага
            #    raise ValidationError('Lastname must be unique. We have "{}" lastname already'.format(new_lastname))

            return new_lastname
"""
