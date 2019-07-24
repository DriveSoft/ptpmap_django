from django import forms
from .models import *
from django.core.exceptions import ValidationError


class PTPForm(forms.ModelForm):
    record_id = forms.IntegerField(required=False) #заносим сюда id записи, для редактирования

    class Meta:
        model = ptp
        fields = ['latitude', 'longitude', 'description', 'datetime', 'ptptype', 'carRedSignal', 'carTurnLeft', 'carTurnRight', 'pedRedSignal', 'pedWrongCross', 'pedKid', 'danger', 'id']





        #widgets = {
        #    'city': forms.Select(attrs={'class': 'form-control'}),
        #}


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
