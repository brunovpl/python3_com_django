from django.conf import settings
from django.shortcuts import render, redirect

from .forms import RegisterForm


def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request=request, context=context, template_name=template_name)
