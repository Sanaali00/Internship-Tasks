from django import forms
from .models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['record_id', 'title', 'description']
