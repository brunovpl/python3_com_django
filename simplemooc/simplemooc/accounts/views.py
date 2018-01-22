from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from .forms import RegisterForm, EditAccountForm


@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    return render(request=request, template_name=template_name)


@login_required
def edit(request):
    template_name = 'accounts/edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            form = EditAccountForm(instance=request.user)
            context['success'] = True
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request=request, template_name=template_name, context=context)


@login_required
def edit_password(request):
    template_name = 'accounts/edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request=request, template_name=template_name, context=context)


def register(request):
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            login(request=request, user=user)
            return redirect('core:home')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request=request, context=context, template_name=template_name)
