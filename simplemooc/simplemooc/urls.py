from django.contrib import admin
from django.urls import path, include

app_name = 'simplemooc'

urlpatterns = [
    path('', include('simplemooc.core.urls', namespace='core')),
    path('cursos/', include('simplemooc.courses.urls', namespace='courses')),
    path('admin/', admin.site.urls),

]
