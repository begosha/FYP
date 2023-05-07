from datetime import datetime

from django import forms

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
        labels = {
            'file': 'file.jpg'
        }

    def save(self, commit=True):
        instance = super(FileForm, self).save(commit=False)
        instance.name = f'file_{id}_{str(datetime.now())}.jpg'
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


class TransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transaction
        fields = ['user', 'positions', 'total_check', 'is_paid']
        widgets = {
            'positions': forms.HiddenInput(),
        }

    def clean_positions(self):
        position_ids = self.data.getlist('positions')
        positions = []
        for position_id in position_ids:
            position = models.Position.objects.get(pk=position_id)
            positions.append({
                'name': position.name,
                'price': position.price
            })
        return positions
