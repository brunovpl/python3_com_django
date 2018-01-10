from django.shortcuts import render, get_object_or_404

from .forms import ContactCourse
from .models import Course


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
            print(form.changed_data)
            form = ContactCourse()
            print(form.changed_data)
    else:
        form = ContactCourse()

    context['course'] = course
    context['form'] = form

    return render(request=request, template_name='courses/details.html', context=context)
