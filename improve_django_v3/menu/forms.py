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

    def clean_expiration_date(self):
        cleaned_data = self.cleaned_data['expiration_date']
        if cleaned_data==None or cleaned_data=='':
            raise forms.ValidationError('Please enter a date and time!')
        return cleaned_data
