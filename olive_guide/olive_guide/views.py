from django.views.generic import TemplateView ,FormView
from django.conf import settings
from django.core.mail import send_mail
from .forms import ContactUsForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

class Home(TemplateView):
    template_name = 'home.html'

class AboutUs(TemplateView):
    template_name = 'about_us.html'


class ContactView(SuccessMessageMixin,FormView):
    form_class = ContactUsForm
    success_message =  _("We received your message we will inform you soon !")
    success_url = '/contact'
    template_name = 'contact.html'
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if self.request.user.is_authenticated:
            form.fields['full_name'].initial = self.request.user.first_name + " " +self.request.user.last_name
            form.fields['email'].initial = self.request.user.email
        return form
    def form_valid(self, form):
        email_subject = form.cleaned_data["subject"]
        email_message = form.cleaned_data["full_name"] + " with the email, " + form.cleaned_data["email"] + ", sent the following message:\n\n" + form.cleaned_data["message"]
        send_mail(email_subject, email_message,  settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
        return super().form_valid(form)
