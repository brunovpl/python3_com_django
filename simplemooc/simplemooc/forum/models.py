from django.conf import settings
from django.db import models
from taggit.managers import TaggableManager


class Thread(models.Model):
    title = models.CharField(verbose_name='Título', max_length=100)
    body = models.TextField(verbose_name='Mensagem')
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='threads')
    views = models.IntegerField(verbose_name='Visualizações', blank=True, default=0)
    answers = models.IntegerField(verbose_name='Respostas', blank=True, default=0)
    tags = TaggableManager()

    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Modificado em', auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-updated_at']


class Reply(models.Model):
    reply = models.TextField(verbose_name='Resposta')
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='replies')

    correct = models.BooleanField(verbose_name='Correta?', blank=True, default=False)
    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Modificado em', auto_now=True)

    def __str__(self):
        return self.reply[:100]
    
    class Meta:
        verbose_name='Resposta'
        verbose_name_plural='Respostas'
        ordering = ['-correct', 'created_at']