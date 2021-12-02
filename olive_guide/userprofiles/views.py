from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserUpdateForm
from django.views.generic import UpdateView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import update_session_auth_hash

class UserUpdateView(SuccessMessageMixin,UpdateView,LoginRequiredMixin):
    model=User
    fields=('username','email','first_name','last_name',)
    success_url = reverse_lazy('user_profile:profile')
    success_message = _("Your profile updated successfully.")
    template_name = 'user_profile_update.html'
    def get_object(self,queryset=None):
        return self.request.user
class ChangePasswordView(SuccessMessageMixin,FormView,LoginRequiredMixin):
    form_class = PasswordChangeForm
    success_message =  _("Your password changed successfully.")
    success_url = reverse_lazy('user_profile:profile')
    template_name = 'user_change_password.html'
    def get_form_kwargs(self):
        kwargs = super(ChangePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)  # Important!
        return super().form_valid(form)
