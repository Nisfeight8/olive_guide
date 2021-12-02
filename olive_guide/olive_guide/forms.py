from django import forms
from django.utils.translation import ugettext_lazy as _

class ContactUsForm(forms.Form):
    full_name=forms.CharField(required=True, label=_('Full Name'),widget=forms.TextInput(attrs={'placeholder': _('Full Name')}))
    email=forms.EmailField(required=True, label=_('Email'),widget=forms.TextInput(attrs={'placeholder': _('Email')}))
    subject=forms.CharField(required=True, label=_('Subject'),widget=forms.TextInput(attrs={'placeholder': _('Subject')}))
    message = forms.CharField(required=True, label=_('Message'),widget=forms.Textarea(attrs={'placeholder': _('Message')}))