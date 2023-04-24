from django import forms
from datetime import datetime
from . import models


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")


class FileForm(forms.ModelForm):
    class Meta:
        model = models.File
        fields = ['file',]
        widgets = {
            'file': forms.FileInput(attrs={'accept': 'image/*', 'capture': 'camera'})
        }

    def save(self, commit=True):
        instance = super(FileForm, self).save(commit=False)
        instance.name = f'file_{id}_{str(datetime.now())}'
        instance.save()
        return instance


class ScanForm(forms.ModelForm):
    class Meta:
        model = models.Scan
        fields = ['image', 'position']


class MailForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        required=True,
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': 'Name'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    subject = forms.CharField(
        max_length=200,
        required=True,
        label='Subject',
        widget=forms.TextInput(attrs={'placeholder': 'Subject'})
    )
    message = forms.CharField(
        max_length=200,
        required=True,
        label='Message',
        widget=forms.TextInput(attrs={'placeholder': 'Message'})
    )

