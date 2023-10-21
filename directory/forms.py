import re
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from directory.utils import check_domain_live
from .models import Directory

class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        fields = ["domain", "category"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['domain'].label = "Website"
    
    def clean_domain(self):
        domain = self.cleaned_data.get('domain')
        # Remove "https://" or "http://" prefixes (case-insensitive)
        domain = re.sub(r'^(https?://)?', '', domain, flags=re.IGNORECASE)
        if domain.endswith('/'):
            domain = domain[:-1]
        domain_pattern = r'^[a-zA-Z0-9.-]*\.[a-zA-Z]{2,}(?:\.(com|net|org))?$'
        is_valid_domain = re.match(domain_pattern, domain)
        print('domain: ', domain)   
        is_domain_live = check_domain_live(f" https://{domain}")
        if is_valid_domain and is_domain_live:
            return domain
        else:
            raise forms.ValidationError("The domain is not valid or not accessible.")
