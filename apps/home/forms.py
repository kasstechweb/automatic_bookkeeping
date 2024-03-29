import os
from django import forms
from django.forms import ValidationError

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        # label='Select a file',
        # help_text='max. 42 megabytes',
        widget=forms.FileInput(attrs={'accept':'application/pdf'})
    )

class DocumentCSVForm(forms.Form):
    docfile = forms.FileField(
        # label='Select a file',
        # help_text='max. 42 megabytes',
        widget=forms.FileInput(attrs={'accept':'application/pdf, .csv', 'multiple': 'multiple'})
    )

class DocumentMultipleForm(forms.Form):
    docfile = forms.FileField(
        # label='Select a file',
        # help_text='max. 42 megabytes',
        widget=forms.FileInput(attrs={'accept':'.csv', 'multiple': 'multiple'})
    )