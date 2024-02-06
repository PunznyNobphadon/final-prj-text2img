from django import forms
from imageaiapp.models import *

class PromptForm(forms.ModelForm):
    class Meta:
        model = Prompt
        fields = ['prompt']