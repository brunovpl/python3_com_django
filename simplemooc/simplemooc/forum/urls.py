from django.urls import path

from simplemooc.forum import views

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<slug:tag>', views.index, name='index_tagged'),
    path('<slug:slug>', views.thread, name='thread'),
    path('respostas/<int:pk>/correta', views.reply_correct, name='reply_correct'),
    path('respostas/<int:pk>/incorreta', views.reply_incorrect, name='reply_incorrect'),
]
