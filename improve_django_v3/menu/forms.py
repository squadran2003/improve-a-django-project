from django import forms

from django.utils.dateparse import parse_datetime

from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ('created_date',)
        widgets = {
            'items':forms.SelectMultiple,
        }
        help_texts = {
            'expiration_date':('e.g 2017-09-19 20:44:00'),
        }

    def clean(self):
        cleaned_data = super(MenuForm, self).clean()
        expiration_date = cleaned_data.get('expiration_date')
        if expiration_date==None or expiration_date=='':
            raise forms.ValidationError('Please enter a valid date and time!')
        return cleaned_data
