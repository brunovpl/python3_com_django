from django.shortcuts import render

from .models import Course


def index(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request=request, template_name='courses/index.html', context=context)


def details(request, pk):
    course = Course.objects.get(pk=pk)
    context = {
        'course': course
    }
    return render(request=request, template_name='courses/details.html', context=context)
