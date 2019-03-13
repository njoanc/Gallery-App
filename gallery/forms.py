from django import forms
from .models import Gallery

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ('description', 'document', )