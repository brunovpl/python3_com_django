from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ContactCourse, CommentForm
from .models import Course, Enrollment, Announcements


def index(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request=request, template_name='courses/index.html', context=context)


def details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {}

    if request.method == 'POST':
        form = ContactCourse(request.POST)
        if form.is_valid():
            context['is_valid'] = True
            form.send_email(course=course)
            form = ContactCourse()
    else:
        form = ContactCourse()

    context['course'] = course
    context['form'] = form

    return render(request=request, template_name='courses/details.html', context=context)


@login_required
def enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)

    if created:
        enrollment.active()
        messages.success(request=request, message='Você foi inscrito no curso com sucesso')
    else:
        messages.info(request=request, message='Você já está inscrito no curso')

    return redirect('accounts:dashboard')


@login_required
def undo_enrollment(request, slug):
    course = get_object_or_404(Course, slug=slug)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request=request, message='Sua inscrição foi cancelada com sucesso')
        return redirect('accounts:dashboard')
    template_name = 'courses/undo_enrollment.html'
    context = {
        'enrollment': enrollment,
        'course': course,
    }
    return render(request=request, template_name=template_name, context=context)


@login_required
def announcements(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
        if not enrollment.is_approved():
            messages.error(request=request, message='Sua inscrição está pendente')
            return redirect('accounts:dashboard')
    template = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request=request, template_name=template, context=context)


@login_required
def show_announcement(request, slug,  pk):
    course = get_object_or_404(Course, slug=slug)
    if not request.user.is_staff:
        enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

        if not enrollment.is_approved():
            messages.error(request=request, message='Sua inscrição está pendente')
            return redirect('accounts:dashboard')

    announcement = get_object_or_404(Announcements, pk=pk)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.announcement = announcement
        comment.save()
        form = CommentForm()
        messages.success(request=request, message='Seu comentário foi enviado com sucesso')

    template_name = 'courses/show_announcement.html'
    announcement = get_object_or_404(course.announcements.all(), pk=pk)
    context = {
        'course': course,
        'announcement': announcement,
        'form': form,
    }

    return render(request=request, template_name=template_name, context=context)
