from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.defaultfilters import striptags
from django.template.loader import render_to_string


def send_mail_template(subject, template_name, context, recipient_list,
                       from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
    message_html = render_to_string(template_name=template_name, context=context)
    message_txt = striptags(value=message_html)

    email = EmailMultiAlternatives(subject=subject, body=message_txt, from_email=from_email, to=recipient_list)
    email.attach_alternative(content=message_html, mimetype="text/html")
    email.send(fail_silently=fail_silently)
