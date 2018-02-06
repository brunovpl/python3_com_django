from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

app_name = 'simplemooc'

urlpatterns = [
    path('', include('simplemooc.core.urls', namespace='core')),
    path('cursos/', include('simplemooc.courses.urls', namespace='courses')),
    path('forum/', include('simplemooc.forum.urls', namespace='forum')),
    path('conta/', include('simplemooc.accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
