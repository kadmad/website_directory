from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from .models import Directory

class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ["domain", "category"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['domain'].label = "Website"