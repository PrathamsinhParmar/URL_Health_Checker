from django import forms
from .models import MonitoredURL


class MonitoredURLForm(forms.ModelForm):
    class Meta:
        model = MonitoredURL
        fields = ['name', 'url', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., My Website',
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'name': 'Display Name',
            'url': 'URL to Monitor',
            'is_active': 'Active (enable monitoring)',
        }

    def clean_url(self):
        url = self.cleaned_data.get('url', '').strip()
        if not (url.startswith('http://') or url.startswith('https://')):
            raise forms.ValidationError(
                'URL must start with http:// or https://'
            )
        return url


from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
