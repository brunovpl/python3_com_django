from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL)
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request=request, context=context, template_name=template_name)
