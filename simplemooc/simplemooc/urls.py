from django.contrib import admin
from django.urls import path, include

app_name = 'simplemooc'

urlpatterns = [
    path('', include('simplemooc.core.urls', namespace='core')),
    path('admin/', admin.site.urls),

]
