from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields=('username','email','first_name','last_name',)
class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label=_('First Name'),widget=forms.TextInput(attrs={'placeholder': _('First Name')}))
    last_name = forms.CharField(max_length=30, label=_('Last Name'),widget=forms.TextInput(attrs={'placeholder': _('Last Name')}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()