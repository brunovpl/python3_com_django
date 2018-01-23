from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ContactCourse
from .models import Course, Enrollment
from django.contrib import messages

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