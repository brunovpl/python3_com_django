from django.urls import path

from simplemooc.forum import views

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<slug:tag>', views.index, name='index_tagged'),
]
