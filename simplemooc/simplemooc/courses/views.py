from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .decorators import enrollment_required
from .forms import ContactCourse, CommentForm
from .models import Course, Enrollment, Announcements, Lesson, Material


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
@enrollment_required
def announcements(request, slug):
    course = request.course
    template = 'courses/announcements.html'
    context = {
        'course': course,
        'announcements': course.announcements.all()
    }
    return render(request=request, template_name=template, context=context)


@login_required
@enrollment_required
def show_announcement(request, slug, pk):
    course = request.course
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


@login_required
@enrollment_required
def lessons(request, slug):
    course = request.course
    lessons = course.release_lessons()
    if request.user.is_staff:
        lessons = course.lessons.all()

    template_name = 'courses/lessons.html'
    context = {
        'course': course,
        'lessons': lessons,
    }

    return render(request=request, template_name=template_name, context=context)


@login_required
@enrollment_required
def lesson(request, slug, pk):
    course = request.course
    lesson = get_object_or_404(Lesson, pk=pk, course=course)

    if not request.user.is_staff and not lesson.is_available():
        messages.error(request=request, message='Esta aula não está disponível')
        return redirect(to='courses:lessons', slug=course.slug)

    template_name = 'courses/lesson.html'
    context = {
        'course': course,
        'lesson': lesson
    }
    return render(request=request, template_name=template_name, context=context)


@login_required
@enrollment_required
def material(request, slug, pk):
    course = request.course
    material = get_object_or_404(klass=Material, lesson__course=course, pk=pk)
    lesson = material.lesson
    if not request.user.is_staff and not lesson.is_available():
        messages.error(request=request, message='Este material não está disponível')
        return redirect(to='courses:lesson', slug=course.slug, pk=lesson.pk)

    if not material.is_embedded():
        return redirect(material.file.url)
    template_name = 'courses/material.html'
    context = {
        'course': course,
        'lesson': lesson,
        'material': material,
    }

    return render(request=request, template_name=template_name, context=context)
