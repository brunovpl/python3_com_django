from django import forms
from django.conf import settings

from simplemooc.core.mail import send_mail_template


class ContactCourse(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    message = forms.CharField(label='Mensagem/Duvida', widget=forms.Textarea)

    def send_email(self, course):
        subject = "[%s] Contato" % course
        context = {
            'name': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'],
        }
        template_name = 'courses/contact_email.html'

        send_mail_template(subject=subject, template_name=template_name, context=context,
                           recipient_list=[settings.CONTACT_EMAIL])
