from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset
from simplemooc.courses.models import Enrollment
User = get_user_model()


@login_required
def dashboard(request):
    template_name = 'accounts/dashboard.html'
    context = {'enrollments': Enrollment.objects.filter(user=request.user)}
    return render(request=request, template_name=template_name, context=context)


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
            messages.success(request=request, message='Os dados da sua conta foram alterados com sucesso')
            return redirect('accounts:dashboard')
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


def password_reset(request):
    template_name = 'accounts/password_reset.html'
    form = PasswordResetForm(request.POST or None)
    context = {}
    if form.is_valid():
        form.save()
        context['success'] = True

    context['form'] = form
    return render(request=request, template_name=template_name, context=context)


def password_reset_confirm(request, key):
    template_name = 'accounts/password_reset_confirm.html'
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    context = {}
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request=request, template_name=template_name, context=context)
