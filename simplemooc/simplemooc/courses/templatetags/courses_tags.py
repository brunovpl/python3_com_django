from django.template import Library

from simplemooc.courses.models import Enrollment

register = Library()


@register.inclusion_tag(filename='courses/templatetags/my_course.html')
def my_courses(user):
    return {'enrollments': Enrollment.objects.filter(user=user)}