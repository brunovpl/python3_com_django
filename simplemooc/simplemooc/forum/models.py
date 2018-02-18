from django.conf import settings
from django.db import models
from django.db.models import CASCADE
from taggit.managers import TaggableManager


class Thread(models.Model):
    title = models.CharField(verbose_name='Título', max_length=100)
    slug = models.SlugField(verbose_name='Identificador', max_length=100, unique=True)
    body = models.TextField(verbose_name='Mensagem')
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='threads',
                               on_delete=CASCADE)
    views = models.IntegerField(verbose_name='Visualizações', blank=True, default=0)
    answers = models.IntegerField(verbose_name='Respostas', blank=True, default=0)
    tags = TaggableManager()

    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Modificado em', auto_now=True)

    def __str__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'forum:thread', (), {'slug': self.slug}

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['-updated_at']


class Reply(models.Model):
    thread = models.ForeignKey(to=Thread, verbose_name='Tópico', related_name='replies', on_delete=CASCADE)
    reply = models.TextField(verbose_name='Resposta')
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Autor', related_name='replies',
                               on_delete=CASCADE)

    correct = models.BooleanField(verbose_name='Correta?', blank=True, default=False)
    created_at = models.DateTimeField(verbose_name='Criado em', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Modificado em', auto_now=True)

    def __str__(self):
        return self.reply[:100]

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'
        ordering = ['-correct', 'created_at']


def post_save_reply(created, instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()
    if instance.correct:
        instance.thread.replies.exclude(pk=instance.pk).update(correct=False)


def post_delete_replay(instance, **kwargs):
    instance.thread.answers = instance.thread.replies.count()
    instance.thread.save()


models.signals.post_save.connect(receiver=post_save_reply, sender=Reply, dispatch_uid='post_save_reply')
models.signals.post_delete.connect(receiver=post_delete_replay, sender=Reply, dispatch_uid='post_delete_replay')
